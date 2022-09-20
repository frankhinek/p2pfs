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
        self.node = Server()
        self.ip = listen_ip
        self.port = listen_port
        self.bootstrap_nodes = bootstrap_nodes

    async def join_network(self) -> None:
        await self.node.listen(self.port, self.ip)
        if self.bootstrap_nodes:
            await self.node.bootstrap(self.bootstrap_nodes)

    def leave_network(self) -> None:
        self.node.stop()

    async def get(self, key):
        return await self.node.get(key)

    async def put(self, key, value):
        return await self.node.set(key, value)