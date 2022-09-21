"""This module manages serving and downloading data between peers.

The module contains the following classes:
- `ContentService` - Serves files to other peers using a simple HTTP server and downloads files via HTTP GET requests.
"""
import logging
from pathlib import Path
import shutil
import urllib
from aiohttp import web, ClientSession

log = logging.getLogger(__name__)

class ContentService:
    def __init__(self, ip: str, port: int, host_root_dir: str, host_url_prefix: str) -> None:
        """Initialize a ContentServer object.

        Args:
            ip (str): Interface IP address this peer should bind to.
            port (int): Port the HTTP server should listen on.
            host_root_dir (str): Local relative path to serve files from.
            host_url_prefix (str): URL path prefix for hosted files.
        """
        self.host_ip = ip
        self.host_port = port
        self.host_root_dir = host_root_dir
        self.host_url_prefix = host_url_prefix

        self.http_app = None
        self.http_site = None
        self.configure_server()

    def configure_server(self) -> None:
        """Instantiate AIOHTTP web application and configure routes.
        """
        self.http_app = web.Application()
        self.http_app.router.add_get('/health', self.health)
        self.http_app.router.add_static(f'/{self.host_url_prefix}', self.host_root_dir)

    def decode_url(self, encoded_url: str) -> str:
        """Utility function uses URLLIB to decode encoded URL.

        Args:
            encoded_url (str): Encoded URL.

        Returns:
            str: Decode URL.
        """
        return urllib.parse.unquote(encoded_url)

    async def delete(self, file_name: str) -> None:
        """Utility function to delete files that are being hosted.

        Args:
            file_name (str): File name to be deleted.
        """
        Path(self.host_root_dir).joinpath(Path(file_name).name).unlink()

    async def get(self, url_list: list, file_list: list, output_dir: str) -> dict:
        """Attempt to download the list of files from one or more hosting
        providers using HTTP GET requests.

        Args:
            url_list (list): List of providers hosting the file(s) for download.
            file_list (list): List of file names to download.
            output_dir (str): Relative path to store the download files in.

        Returns:
            dict: _description_
        """
        download_results = {}
        chunk_size = 16*1024
        # Iteratively download each file, trying the URLs in order until one succeeds.
        for file in file_list:
            download_results[file['name']] = False
            output_path = Path(output_dir).joinpath(Path(file['name']))
            for url_path in url_list:
                url = urllib.parse.unquote(url_path + file['name'])
                try:
                    async with ClientSession() as session:
                        async with session.get(url) as resp:
                            with open(output_path, 'wb') as fd:
                                async for chunk in resp.content.iter_chunked(chunk_size):
                                    fd.write(chunk)
                    # If the file is downloaded successfully, skip the rest of the URls and proceed to the next file.
                    download_results[file['name']] = True
                    break
                except Exception as e:
                    log.warning(f'Download failed from: {url}')
                    
        return download_results

    def get_encoded_url_path(self) -> str:
        """Returns the base URL path for files hosted by this peer.

        Returns:
            str: URL encoded base path.
        """
        url = f'http://{self.host_ip}:{self.host_port}/{self.host_url_prefix}/'
        return urllib.parse.quote(url)

    async def health(self, request: dict) -> web.Response:
        """Health endpoint to check if the HTTP service is running.

        Args:
            request (dict): HTTP request object.

        Returns:
            web.Response: HTTP response object.
        """
        return web.json_response({"status":"OK"})

    def put(self, src_file_path: str) -> bool:
        """Copies files from source content directory to the HTTP server's root
        directory to be served to peers that issue HTTP GET requests to download.

        Args:
            src_file_path (str): Path to the source file to be copied to the server root directory.

        Returns:
            bool: True if copy succeeded, False otherwise.
        """
        file_name = Path(src_file_path).name
        dst_file_path = Path(self.host_root_dir).joinpath(Path(file_name))
        result = shutil.copy2(src_file_path, dst_file_path)
        return True if result else False

    async def start_serving(self) -> None:
        """Start AIOHTTP server and listen for requests.
        """
        runner = web.AppRunner(self.http_app)
        await runner.setup()
        self.http_site = web.TCPSite(runner, self.host_ip, self.host_port)
        await self.http_site.start()

    async def stop_serving(self) -> None:
        """Stop AIOHTTP server.
        """
        await self.http_site.stop()