import pytest
from p2pfs.dht import DHT


@pytest.mark.asyncio
async def test_bootstrap(bootstrap_peer_config):
    peer_bootstrap = DHT(bootstrap_peer_config['HOST_IP_ADDRESS'],
                         bootstrap_peer_config['DHT_LISTEN_PORT'],
                         bootstrap_peer_config['DHT_BOOTSTRAP_NODES'])
    await peer_bootstrap.join_network()
    peer_bootstrap.leave_network()


@pytest.mark.asyncio
async def test_two_peers(bootstrap_peer_config, peer2_config):
    peer_bootstrap = DHT(bootstrap_peer_config['HOST_IP_ADDRESS'],
                         bootstrap_peer_config['DHT_LISTEN_PORT'],
                         bootstrap_peer_config['DHT_BOOTSTRAP_NODES'])
    peer2 = DHT(peer2_config['HOST_IP_ADDRESS'],
                peer2_config['DHT_LISTEN_PORT'],
                peer2_config['DHT_BOOTSTRAP_NODES'])

    await peer_bootstrap.join_network()
    await peer2.join_network()

    peer2.leave_network()
    peer_bootstrap.leave_network()


@pytest.mark.asyncio
async def test_set_get(bootstrap_peer_config, peer2_config):
    peer_bootstrap = DHT(bootstrap_peer_config['HOST_IP_ADDRESS'],
                         bootstrap_peer_config['DHT_LISTEN_PORT'],
                         bootstrap_peer_config['DHT_BOOTSTRAP_NODES'])
    peer2 = DHT(peer2_config['HOST_IP_ADDRESS'],
                peer2_config['DHT_LISTEN_PORT'],
                peer2_config['DHT_BOOTSTRAP_NODES'])

    await peer_bootstrap.join_network()
    await peer2.join_network()

    k, v = 'key', 'value'
    put_result = await peer_bootstrap.put(k, v)
    get_result = await peer_bootstrap.get(k)

    assert put_result == True  # Put was successful.
    assert get_result == v     # Value returned matched what was set.

    peer2.leave_network()
    peer_bootstrap.leave_network()