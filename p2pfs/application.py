"""This module implementations the Application layer of a 3-layer design that includes UI and Network layers.

The Application layer provides a UI layer client with services to search for files, publish files to share, and
initiate file downloads.  It manages the DHT and ContentService components that make up the Network layer.

The module contains the following classes:
- `QueryService` - Queries the DHT for files by file name or metadata tags.
- `IndexingService` - Extract metadata from files and inserts mappings from metadata tags to content IDs into the DHT.
"""
from p2pfs.network import ContentService
import dag_cbor
from p2pfs.dht import DHT
import logging
from pathlib import Path
from tinytag import TinyTag

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.addHandler(handler)
log.setLevel(logging.DEBUG)

# loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
# for logger in loggers:
#     logger.addHandler(handler)
#     logger.setLevel(logging.DEBUG)


class Application:
    def __init__(self, config: dict) -> None:
        """Initialize the Application layer.

        If this peer is starting a new network, set `DHT_BOOTSTRAP_NODES` to an empty list.
        If this peer is joining and existing network, specify one or more bootstrap nodes.

        Application Configuration:
        - `HOST_IP_ADDRESS` - Interface IP address this peer should bind to.
        - `HOST_PORT` - Port this peer should listen on for HTTP GET requests to download files.
        - `HOST_ROOT_DIR` - Local relative path to serve files from.
        - `HOST_URL_PREFIX` - URL path prefix for hosted files.
        - `DHT_LISTEN_PORT` - Port the DHT overlay should listen on.
        - `DHT_BOOTSTRAP_NODES` - (Optional) List of (ip, port) tuples to join.
        - `CONTENT_DIR` - Relative or full path to store content available to publish or after downloading.

        Args:
            config (dict): Application configuration specified as keys/values.
        """
        ## Initialize Networking layer services.
        self._dht = DHT(config['HOST_IP_ADDRESS'], config['DHT_LISTEN_PORT'], config['DHT_BOOTSTRAP_NODES'])
        self._content = ContentService(config['HOST_IP_ADDRESS'], config['HOST_PORT'], config['HOST_ROOT_DIR'], config['HOST_URL_PREFIX'])

        # Initialize Application layer services
        self.content_dir = config['CONTENT_DIR']
        self._indexing = IndexingService(self._dht)
        self._query = QueryService(self._dht)
    
    async def start(self) -> None:
        """Start the DHT overlay and ContentService server.
        """
        await self._dht.join_network()
        await self._content.start_serving()

    async def stop(self) -> None:
        """Stop the DHT overlay and ContentService server.
        """
        self._dht.leave_network()
        await self._content.stop_serving()

    async def publish(self, file_name: str) -> bool:
        """Inserts the file's content ID and metadata tags into the DHT.
        Calls ContentService to start serving the file.

        Examples:
            >>> peer.publish('Pearl Jam - Go.mp3')
            True

        Args:
            file_name (str): File name to publish.

        Returns:
            bool: Returns True if the DHT inserts and content serving were successful, else False.
        """
        file_path = Path(self.content_dir).joinpath(Path(file_name))
        url_path = self._content.get_encoded_url_path()
        insert_result = await self._indexing.put(file_path, url_path)

        if all(insert_result):
            return self._content.put(file_path)
        else:
            log.error('Failed to insert file and metadata tags into DHT')
            return False

    async def search(self, field: str, term: str) -> dict:
        """Search the DHT for keys matching the search field and term.
        Used to look up files by album, artist, track, or filename.

        Examples:
            >>> app.search('title', 'Radar Love')

        Args:
            field (str): Search field to query with.
            term (str): Search term to query with

        Returns:
            dict | None: If search result is found, return metadata information. Otherwise, return empty dictionary.
        """
        return await self._query.query(field, term)

    async def download(self, url_list: list, file_list: list) -> dict:
        """Attempt to download the list of files from one or more hosting
        providers.

        Args:
            url_list (list): List of providers hosting the file(s) for download.
            file_list (list): List of file names to download.

        Returns:
            dict: Keys are file names and values are success (True) are failure (False).
        """
        return await self._content.get(url_list, file_list, self.content_dir)

class IndexingService:
    """Extract metadata from files and inserts mappings from metadata tags to
    content IDs into the DHT.
    """

    def __init__(self, dht: DHT) -> None:
        """Initialize the Indexing Service to be managed by the Application layer.

        Args:
            dht (DHT): DHT class object instantiated by the managing Application.
        """
        self.dht = dht

    def get_metadata(self, file_path: str) -> dict:
        """Reads ID3 metadata from media files and returns select tags:
        - file name
        - album
        - artist
        - song title

        Args:
            file_path (str): Relative path to the file.

        Returns:
            dict: Extracted file name, album, artist, and title.
        """
        tag = TinyTag.get(file_path)
        return {
            'filename': Path(file_path).name,
            'album': tag.album,
            'artist': tag.artist,
            'title': tag.title
        }

    def generate_tags(self, metadata: dict) -> list:
        """Takes as input a dictionary of file metadata tag names and their values
        and returns a list string keys to insert into the DHT.

        Args:
            metadata (dict): File metadata tags as keys and the values for a file.

        Examples:
            >>> is.generate_tags({'artist': 'Pearl Jam', 'title': 'Go'})
            ['artist|Pearl Jam', 'title|Go']

        Returns:
            list: Pipe deliminted search keys.
        """
        return [f'{k}|{v}' for k, v in metadata.items()]

    async def put(self, file_path: str, url_path: str) -> list:
        """Insert's the file's content ID and metadata tags into the DHT.

        Args:
            file_path (str): Relative path to the file to publish.
            url_path (str): Base URL path at which the file will be served for peers to download.

        Returns:
            list(bool): List of results from the publish operations, True if succeeded, False if failed.
        """
        index_tasks = []

        # Use the hash of the file to address the contents.
        file_bytes = Path(file_path).read_bytes()
        content_id = self.dht.hash_digest(file_bytes)

        # Check to see if any peers already host the file contents before publishing.
        metainfo_cbor = await self.dht.get(content_id)
        if metainfo_cbor:
            # File is already hosted.
            metainfo = dag_cbor.decode(metainfo_cbor)
            if url_path not in metainfo['url-list']:
                # This node isn't already on list of providers, add it and update key/value in DHT.
                metainfo['url-list'].append(url_path)
                metainfo_cbor = dag_cbor.encode(metainfo)
                index_tasks.append(self.dht.put(content_id, metainfo_cbor))
            
        else:
            # File has never been hosted before.
            metadata = self.get_metadata(file_path)
            files = [{'name': Path(file_path).name, 'cid': content_id}]
            metainfo = {'metadata': metadata, 'files': files, 'url-list': [url_path]}

            # Insert the content addressable file hash and metainfo into the DHT.
            metainfo_cbor = dag_cbor.encode(metainfo)
            index_tasks.append(self.dht.put(content_id, metainfo_cbor))

            # Add metadata tag updates to insert into the DHT.
            index_tasks.extend([self.dht.put(k, content_id) for k in self.generate_tags(metadata)])

        if index_tasks:
            # Run DHT inserts concurrently.
            return await self.dht.put_collection(index_tasks)
        else:
            log.info(f'publish skipped for already published file: {file_path}')
            return [False]


class QueryService:
    """Queries the DHT for files by file name or metadata tags.
    """
    def __init__(self, dht: DHT) -> None:
        """Initialize the Query Service to be managed by the Application layer.

        Args:
            dht (DHT): DHT class object instantiated by the managing Application.
        """
        self.dht = dht
    
    async def query(self, field: str, term: str) -> dict:
        """Query the DHT for the specified field and term.
        If a result is found, query the DHT again to retrieve the
        metainfo.

        Examples:
            >>> qsvc.query('title', 'Radar Love')
            {
                'metadata': {
                    'filename': 'Golden Earring - Radar Love.mp3',
                    'album': 'Moontan',
                    'artist': 'Golden Earring',
                    'title': 'Radar Love'
                },
                'url-list': [
                    'http%3A//0.0.0.0%3A8080/download/Golden%20Earring%20-%20Radar%20Love.mp3'
                ]
            }

        Args:
            field (str): Search field to query with.
            term (str): Search term to query with

        Returns:
            dict | None: If search result is found, return metadata information. Otherwise, return empty dictionary.
        """
        # Get the content address, if any results.
        content_id_found = await self.dht.get(f'{field}|{term}')
        if content_id_found:
            # Retrieve metainfo for content address.
            file_metainfo_cbor = await self.dht.get(content_id_found)
            if file_metainfo_cbor:
                file_metainfo = dag_cbor.decode(file_metainfo_cbor)
                return file_metainfo
        return {}