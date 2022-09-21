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
    return 'Tchaikovsky - Nutcracker by Jon Sayles.mp3'

@pytest.fixture
def content_file_2():
    return 'Rafael Krux - Ukulele Song.mp3'

@pytest.fixture
def example_metainfo():
    return {
        'metadata': {
            'filename': 'Golden Earring - Radar Love.mp3',
            'album': 'Moontan',
            'artist': 'Golden Earring',
            'title': 'Radar Love'
        },
        'url-list': [
            'http%3A//0.0.0.0%3A8080/download/Golden%20Earring%20-%20Radar%20Love.mp3'
        ]
    }