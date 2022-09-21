"""This module implements peer and content routing as a DHT overlay.

The implementation uses a facade design pattern to enable swapping out the routing protocol implementation.
This prototype uses the popular DHT protocol, Kademlia, which is used by BitTorrent and IPFS.

The module contains the following classes:
- `DHT` - Wrapper for the `kademlia` package implementation of a DHT peer-to-peer overlay.
"""
import asyncio
from kademlia.utils import digest
import logging
from kademlia.network import Server

# For the get_digest method addition:
from kademlia.node import Node
from kademlia.crawling import ValueSpiderCrawl

log = logging.getLogger(__name__)

class ServerWithGetDigest(Server):
    """Extend the `kademlia.network` `Server` class with a `get_digest()` method
    that permits getting the value by hash digest key instead of just str that
    is supported by the existing `Server.get()` method.
    """
    async def get_digest(self, dkey):
        """
        Get a key if the network has it.

        Returns:
            :class:`None` if not found, the value otherwise.
        """
        # if this node has it, return it
        if self.storage.get(dkey) is not None:
            return self.storage.get(dkey)
        node = Node(dkey)
        nearest = self.protocol.router.find_neighbors(node)
        if not nearest:
            log.warning("There are no known neighbors to get key %s", dkey)
            return None
        spider = ValueSpiderCrawl(self.protocol, node, nearest,
                                    self.ksize, self.alpha)
        return await spider.find()


class DHT:
    def __init__(self, listen_ip: str, listen_port: int, bootstrap_nodes: list | None = None) -> None:
        """Initialize DHT overlay.

        Args:
            listen_ip (str): Interface IP address the DHT overlay will bind to.
            listen_port (int): UDP port the DHT overlay will listen on.
            bootstrap_nodes (list | None, optional): One or more bootstrap nodes to connect to as (ip: str, port: int) tuples. Defaults to None.
        """
        self.node = ServerWithGetDigest()
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

    def hash_digest(self, value: str) -> bytes:
        """Returns the SHA1 hash of the input value.

        Args:
            value (str): Value to be passed through the hash function.

        Returns:
            bytes: Hash digest of the input value.
        """
        return digest(value)

    async def get(self, key: str) -> str | None:
        """Lookup a key in the DHT overlay, and if found, retrieve the stored value.

        Args:
            key (str): Key to look up.

        Returns:
            str | None: String value, if found, or None if not found in DHT.
        """
        if isinstance(key, bytes):
            return await self.node.get_digest(key)
        return await self.node.get(key)

    async def put(self, key: str, value: str) -> bool:
        """Insert a key/value into the DHT overlay.

        Args:
            key (str): Key to insert.
            value (str): Value to set for key.

        Returns:
            bool: Result of the insert operation.
        """
        if isinstance(key, bytes):
            return await self.node.set_digest(key, value)
        return await self.node.set(key, value)

    async def put_collection(self, task_list: list) -> list:
        """Concurrently perform multiple `put` insertion operations.
        Returns true for each coroutine that is executed successfully and false otherwise.

        Args:
            task_list (list): List of Asyncio coroutines.

        Returns:
            list: A list of bool values, one for each coroutine result.
        """
        return await asyncio.gather(*task_list, return_exceptions=True)
