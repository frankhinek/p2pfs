"""This module implements peer and content routing as a DHT overlay.

The implementation uses a facade design pattern to enable swapping out the routing protocol implementation.
This prototype uses the popular DHT protocol, Kademlia, which is used by BitTorrent and IPFS.

The module contains the following classes:
- `DHT` - Wrapper for the `kademlia` package implementation of a DHT peer-to-peer overlay.
"""
import logging
from kademlia.network import Server

log = logging.getLogger(__name__)

class DHT:
    def __init__(self, listen_ip: str, listen_port: int, bootstrap_nodes: list | None = None) -> None:
        """Initialize DHT overlay.

        Args:
            listen_ip (str): Interface IP address the DHT overlay will bind to.
            listen_port (int): UDP port the DHT overlay will listen on.
            bootstrap_nodes (list | None, optional): One or more bootstrap nodes to connect to as (ip: str, port: int) tuples. Defaults to None.
        """
        self.node = Server()
        self.ip = listen_ip
        self.port = listen_port
        self.bootstrap_nodes = bootstrap_nodes

    async def join_network(self) -> None:
        """Starts the DHT overlay listening on the specified port and interface address.
        If this is the first node in the network, the `bootstrap_nodes` list should be
        empty so that the node starts a new network.  If joining an existing overlay 
        network, the `DHT` class should be initialized with a list of one or more
        bootstrap nodes to connect to.
        """
        await self.node.listen(self.port, self.ip)
        if self.bootstrap_nodes:
            await self.node.bootstrap(self.bootstrap_nodes)

    def leave_network(self) -> None:
        """Shuts down the DHT overlay and stops listening for datagrams.
        """
        self.node.stop()

    async def get(self, key: str) -> str | None:
        """Lookup a key in the DHT overlay, and if found, retrieve the stored value.

        Args:
            key (str): Key to look up.

        Returns:
            str | None: String value, if found, or None if not found in DHT.
        """
        return await self.node.get(key)

    async def put(self, key: str, value: str) -> bool:
        """Insert a key/value into the DHT overlay.

        Args:
            key (str): Key to insert.
            value (str): Value to set for key.

        Returns:
            bool: Result of the insert operation.
        """
        return await self.node.set(key, value)
