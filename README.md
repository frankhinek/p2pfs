# Peer-to-Peer File Sharing Prototype

## Introduction

The `p2pfs` project is a prototype of a peer-to-peer file sharing system.  A decentralized, trackerless design
was implemented using a Distributed Hash Table (DHT) overlay that provides peer and content routing.  While a
modular design was used to facilitate swapping out the overlay protocol implementation, this prototype was built
on the [kademlia](https://github.com/bmuller/kademlia) package, an asynchronous Python implementation of the
[Kademlia protocol](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf).

This prototype was built over the course of a 36-hour personal hackathon, and as such, is very basic in terms of features, implementation robustness, and extensive unit/e2e tests.  Potential feature improvements to be made include:

1. Enhance the network layer services to include:
    - encryption with SSL
    - additional transport protocols beyond a simple HTTP server
    - NAT traversal (hole punching, port mapping, and relay)
    - CRC32 check in the meta-info file to verify download integrity.

2. Chunk content to enable parallel downloads from multiple peers:
    - Break files into 256KB or 512KB chunks
    - Hash the chunks and insert these content IDs into the DHT overlay

3. Improve security and resistance to threats, including:
    - attacks on overlay routing (e.g., eclipse attack, sybil attack, churn based attacks, and adversarial routing)
    - attacks on p2p applications built on this stack (e.g., DDoS, content hosting, data storage)

4. Extend the QueryService and IndexService to support multiple results for tag|search searches.

## Background

The [Kademlia protocol](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf) was developed by 
Petar Maymounkov and David Mazières.

With Kademlia, an overlay network is formed by peers in which each node is given a unique 160-bit identifier.
File hashes and keywords are inserted into the same identifier space, and Kademlia uses a novel XOR distance metric
to enable nodes to efficiently, _O(log(n))_, lookup keys.

Kademlia is also used by projects such as IPFS, BitTorrent, and I2P.

## Acknowledgements

- Petar Maymounkov and David Mazières for the publication of the
[Kademlia protocol](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf) paper in 2002.
- [Brian Muller](https://github.com/bmuller/) for the [kademlia](https://github.com/bmuller/kademlia) Python library.