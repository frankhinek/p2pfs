import pytest

@pytest.fixture
def bootstrap_peer_config():
    return {
        'CONTENT_DIR': 'content',
        'DHT_BOOTSTRAP_NODES': [],
        'DHT_LISTEN_PORT': 6881,
        'HOST_IP_ADDRESS': '0.0.0.0',
        'HOST_PORT': 8080,
        'HOST_ROOT_DIR': 'http_root',
        'HOST_URL_PREFIX': 'download',
    }

@pytest.fixture
def peer2_config():
    return {
        'CONTENT_DIR': 'content',
        'DHT_BOOTSTRAP_NODES': [('0.0.0.0', 6881)],
        'DHT_LISTEN_PORT': 6882,
        'HOST_IP_ADDRESS': '0.0.0.0',
        'HOST_PORT': 8081,
        'HOST_ROOT_DIR': 'http_root',
        'HOST_URL_PREFIX': 'download',
    }


@pytest.fixture
def peer3_config():
    return {
        'DHT_BOOTSTRAP_NODES': [('0.0.0.0', 6881)],
        'DHT_LISTEN_PORT': 6883,
        'CONTENT_DIR': 'content',
        'HOST_IP_ADDRESS': '0.0.0.0',
        'HOST_PORT': 8082,
        'HOST_ROOT_DIR': 'http_root',
        'HOST_URL_PREFIX': 'download',
    }

@pytest.fixture
def content_file_1():
    return 'Pearl Jam - Go.mp3'

@pytest.fixture
def content_file_2():
    return 'Golden Earring - Radar Love.mp3'
