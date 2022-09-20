"""Prototype implementation of a peer-to-peer file sharing application.

Modules exported by this package:

- `application`: Queries for files to retrieve, indexes published files, and initiates file transfers.
- `dht`: Wrapper for the DHT implementation used for the peer-to-peer overlay.
- `network`: Manages transporting data between peers.
"""