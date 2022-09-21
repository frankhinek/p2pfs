import pytest
from p2pfs.application import Application

@pytest.mark.asyncio
@pytest.mark.parametrize(['field', 'search_term'], [('artist', 'Tchaikovsky'), ('title', 'Nutcracker (Dance of the Sugar Plum Fairy)'), ('album', 'Jon Sayles'), ('filename', 'Tchaikovsky - Nutcracker by Jon Sayles.mp3')])
async def test_search_by(bootstrap_peer_config, peer2_config, content_file_1, field, search_term):
    # Note: The `kademlia` package requires at least two nodes to be online
    # before allowing a key/value to be set.
    peer_bootstrap = Application(bootstrap_peer_config)
    peer2 = Application(peer2_config)

    await peer_bootstrap.start()
    await peer2.start()

    # Peer 2 publish file to DHT.
    file_to_publish = content_file_1
    await peer2.publish(file_to_publish)
    
    # Verify Peer 1 knows about the published file.
    result_metainfo = await peer_bootstrap.search(field, search_term)
    assert search_term == result_metainfo['metadata'][field]

    # Clean Up before next test run
    await peer2.stop()
    await peer_bootstrap.stop()


@pytest.mark.asyncio
async def test_query_with_no_results(bootstrap_peer_config, peer2_config):
    # Note: The `kademlia` package requires at least two nodes to be online
    # before allowing a key/value to be set.
    peer_bootstrap = Application(bootstrap_peer_config)
    peer2 = Application(peer2_config)

    await peer_bootstrap.start()
    await peer2.start()

    # Verify search returns no results.
    result_metainfo = await peer_bootstrap.search('Never', 'Heard of it')
    assert bool(result_metainfo) == False

    # Clean Up before next test run
    await peer2.stop()
    await peer_bootstrap.stop()
