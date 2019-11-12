import pytest

def test_first_endpoint(client):
    """Start with a blank database."""

    resp = client.get('/testing')
    assert resp.status_code == 406,"The testing enpoind has to return 406"