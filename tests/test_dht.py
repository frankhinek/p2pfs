import pytest
from p2pfs.application import Application

@pytest.mark.asyncio
async def test_bootstrap(bootstrap_peer_config):
    peer_bootstrap = Application(bootstrap_peer_config)
    await peer_bootstrap.start()

    await peer_bootstrap.stop()


@pytest.mark.asyncio
async def test_two_peers(bootstrap_peer_config, peer2_config):
    peer_bootstrap = Application(bootstrap_peer_config)
    await peer_bootstrap.start()

    peer2 = Application(peer2_config)
    await peer2.start()

    await peer2.stop()
    await peer_bootstrap.stop()


@pytest.mark.asyncio
async def test_three_peers(bootstrap_peer_config, peer2_config, peer3_config):
    peer_bootstrap = Application(bootstrap_peer_config)
    await peer_bootstrap.start()

    peer2 = Application(peer2_config)
    await peer2.start()

    peer3 = Application(peer3_config)
    await peer3.start()

    await peer3.stop()
    await peer2.stop()
    await peer_bootstrap.stop()
