import pytest
from p2pfs.application import IndexingService

def test_generate_tags():
    metadata = {
        'filename': 'Pearl Jam - Go.mp3',
        'album': 'Vs.',
        'artist': 'Pearl Jam',
        'title': 'Go',
    }

    indexing_svc = IndexingService(None)
    result = indexing_svc.generate_tags(metadata)
    
    assert result == [
        'filename|Pearl Jam - Go.mp3',
        'album|Vs.',
        'artist|Pearl Jam',
        'title|Go',
    ]