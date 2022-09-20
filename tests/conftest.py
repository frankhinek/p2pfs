import pytest

@pytest.fixture
def bootstrap_peer_config():
    return {
        'HOST_IP_ADDRESS': '0.0.0.0',
        'DHT_LISTEN_PORT': 6881,
        'DHT_BOOTSTRAP_NODES': []
    }

@pytest.fixture
def peer2_config():
    return {
        'HOST_IP_ADDRESS': '0.0.0.0',
        'DHT_LISTEN_PORT': 6882,
        'DHT_BOOTSTRAP_NODES': [('0.0.0.0', 6881)]
    }


@pytest.fixture
def peer3_config():
    return {
        'HOST_IP_ADDRESS': '0.0.0.0',
        'DHT_LISTEN_PORT': 6883,
        'DHT_BOOTSTRAP_NODES': [('0.0.0.0', 6881)]
    }
