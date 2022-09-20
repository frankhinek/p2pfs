"""This module implementations the Application layer of a 3-layer design that includes UI and Network layers.

The Application layer provides a UI layer client with services to search for files, publish files to share, and
initiate file downloads.  It manages the DHT and ContentService components that make up the Network layer.

The module contains the following classes:
- `QueryService` - Queries the DHT for files by file name or metadata tags.
- `IndexingService` - Extract metadata from files and inserts mappings from metadata tags to content IDs into the DHT.
"""
from p2pfs.dht import DHT
import logging

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
        - `DHT_LISTEN_PORT` - Port the DHT overlay should listen on.
        - `DHT_BOOTSTRAP_NODES` - (Optional) List of (ip, port) tuples to join.

        Args:
            config (dict): Application configuration specified as keys/values.
        """
        ## Initialize Networking layer services.
        self._dht = DHT(config['HOST_IP_ADDRESS'], config['DHT_LISTEN_PORT'], config['DHT_BOOTSTRAP_NODES'])
    
    async def start(self) -> None:
        """Start the DHT overlay.
        """
        await self._dht.join_network()

    async def stop(self) -> None:
        """Stop the DHT overlay.
        """
        self._dht.leave_network()
