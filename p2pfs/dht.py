"""This module implements peer and content routing as a DHT overlay.

The implementation uses a facade design pattern to enable swapping out the routing protocol implementation.
This prototype uses the popular DHT protocol, Kademlia, which is used by BitTorrent and IPFS.

The module contains the following classes:
- `DHT` - Wrapper for the `kademlia` package implementation of a DHT peer-to-peer overlay.
"""