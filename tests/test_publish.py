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
    await peer_bootstrap.publish(file_to_publish)

    # Peer 2 publish file to DHT.
    file_to_publish = content_file_2
    await peer2.publish(file_to_publish)
    
    await peer2.stop()
    await peer_bootstrap.stop()


@pytest.mark.asyncio
async def test_verify_published(bootstrap_peer_config, peer2_config, content_file_1):
    peer_bootstrap = Application(bootstrap_peer_config)
    peer2 = Application(peer2_config)

    await peer_bootstrap.start()
    await peer2.start()

    # Peer 2 publish file to DHT.
    file_to_publish = content_file_1
    await peer2.publish(file_to_publish)
    
    # Verify Peer 1 knows about the published file.
    result_metainfo = await peer_bootstrap.search('filename', file_to_publish)
    assert file_to_publish == result_metainfo['metadata']['filename']

    await peer2.stop()
    await peer_bootstrap.stop()


@pytest.mark.asyncio
async def test_two_providers(bootstrap_peer_config, peer2_config, content_file_1):
    peer_bootstrap = Application(bootstrap_peer_config)
    peer2 = Application(peer2_config)

    await peer_bootstrap.start()
    await peer2.start()

    file_to_publish = content_file_1

    # Peer 1 publish file to DHT.
    await peer_bootstrap.publish(file_to_publish)

    # Peer 2 publish file to DHT.
    await peer2.publish(file_to_publish)
    
    # Verify Peer 1 knows about two providers of a single file.
    result_metainfo = await peer_bootstrap.search('filename', file_to_publish)
    assert len(result_metainfo['url-list']) == 2
    assert len(result_metainfo['files']) == 1

    await peer2.stop()
    await peer_bootstrap.stop()


@pytest.mark.asyncio
async def test_published_url(bootstrap_peer_config, peer2_config, content_file_1):
    peer_bootstrap = Application(bootstrap_peer_config)
    peer2 = Application(peer2_config)

    await peer_bootstrap.start()
    await peer2.start()

    # Peer 2 publish file to DHT.
    file_to_publish = content_file_1
    await peer2.publish(file_to_publish)
    
    # Verify Peer 1 knows about the published file.
    result_metainfo = await peer_bootstrap.search('filename', file_to_publish)
    import urllib
    expected_url = f"http://{peer2_config['HOST_IP_ADDRESS']}:{peer2_config['HOST_PORT']}/{peer2_config['HOST_URL_PREFIX']}/"
    assert urllib.parse.unquote(result_metainfo['url-list'][0]) == expected_url

    await peer2.stop()
    await peer_bootstrap.stop()