import pytest
from p2pfs.application import Application

@pytest.mark.asyncio
async def test_publish(bootstrap_peer_config, peer2_config, content_file_1, content_file_2):
    peer_bootstrap = Application(bootstrap_peer_config)
    peer2 = Application(peer2_config)

    await peer_bootstrap.start()
    await peer2.start()

    # Peer 1 publish file to DHT.
    file_to_publish = content_file_1
    await peer2.publish(file_to_publish)

    # Peer 2 publish file to DHT.
    file_to_publish = content_file_2
    await peer2.publish(file_to_publish)
    
    await peer2.stop()
    await peer_bootstrap.stop()
