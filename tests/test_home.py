import pytest
from mywebsite.db import get_db


def test_index(client):
    response = client.get('/')
    assert b"Mason McGough" in response.data
    assert b"Home" in response.data
