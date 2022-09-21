from p2pfs.network import ContentService
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
