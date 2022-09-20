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
        ## Initialize Networking layer services.
        self._dht = DHT(config['HOST_IP_ADDRESS'], config['DHT_LISTEN_PORT'], config['DHT_BOOTSTRAP_NODES'])
    
    async def start(self) -> None:
        await self._dht.join_network()

    async def stop(self) -> None:
        self._dht.leave_network()
