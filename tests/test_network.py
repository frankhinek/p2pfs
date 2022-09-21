from p2pfs.application import Application
from p2pfs.network import ContentService
import pytest
import urllib

def test_encoded_url_path(bootstrap_peer_config):
    host_ip = bootstrap_peer_config['HOST_IP_ADDRESS']
    host_port = bootstrap_peer_config['HOST_PORT']
    host_url_prefix = bootstrap_peer_config['HOST_URL_PREFIX']
    content_svc = ContentService(host_ip, host_port, '', host_url_prefix)

    expected_result = urllib.parse.quote(
        f'http://{host_ip}:{host_port}/{host_url_prefix}/'
    )
    assert content_svc.get_encoded_url_path() == expected_result

@pytest.mark.asyncio
async def test_health_endpoint(bootstrap_peer_config, aiohttp_client):
    host_ip = bootstrap_peer_config['HOST_IP_ADDRESS']
    host_port = bootstrap_peer_config['HOST_PORT']
    host_url_prefix = bootstrap_peer_config['HOST_URL_PREFIX']
    content_svc = ContentService(host_ip, host_port, '', host_url_prefix)
    await content_svc.start_serving()

    client = await aiohttp_client(content_svc.http_app)
    resp = await client.get('/health')
    assert resp.status == 200
    json_data = await resp.json()
    assert json_data == {'status': 'OK'}

    await content_svc.stop_serving()

@pytest.mark.asyncio
async def test_static_content(bootstrap_peer_config, peer2_config, content_file_1, aiohttp_client):
    peer_bootstrap = Application(bootstrap_peer_config)
    peer2 = Application(peer2_config)

    await peer_bootstrap.start()
    await peer2.start()

    # Peer 2 publish file to DHT.
    file_to_publish = content_file_1
    await peer2.publish(file_to_publish)

    client = await aiohttp_client(peer2._content.http_app)

    url = f'{peer2._content.host_url_prefix}/{file_to_publish}'
    resp = await client.get(url)
    assert resp.status == 200
    assert resp.content_type == 'audio/mpeg'
    assert resp.content_length > 1024*1024
    data = await resp.read()
    assert isinstance(data, bytes)

    await peer2.stop()
    await peer_bootstrap.stop()