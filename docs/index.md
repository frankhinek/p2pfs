# Peer-to-Peer File Transfer Prototype

This site contains the project documentation for the `p2pfs` project, which is a prototype of a
peer-to-peer file sharing system.  A decentralized, trackerless design was implemented using a
Distributed Hash Table (DHT) overlay that provides peer and content routing.  While a modular design was
used to facilitate swapping out the overlay protocol implementation, this prototype was built on the
[kademlia](https://github.com/bmuller/kademlia) package, an asynchronous Python implementation of the
[Kademlia protocol](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf) developed by 
Petar Maymounkov and David Mazières.  Kademlia is also used by projects such as IPFS, BitTorrent, and I2P.

With Kademlia, an overlay network is formed by peers in which each node is given a unique 160-bit identifier.
File hashes and keywords are inserted into the same identifier space, and Kademlia uses a novel XOR distance metric
to enable nodes to efficiently, _O(log(n))_, lookup keys.

## Table Of Contents

The documentation follows the best practice for
project documentation as described by Daniele Procida
in the [Diátaxis documentation framework](https://diataxis.fr/)
and consists of four separate parts:

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

## Acknowledgements

- Petar Maymounkov and David Mazières for the publication of the
[Kademlia protocol](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf) paper in 2002.
- [Brian Muller](https://github.com/bmuller/) for the [kademlia](https://github.com/bmuller/kademlia) Python library.