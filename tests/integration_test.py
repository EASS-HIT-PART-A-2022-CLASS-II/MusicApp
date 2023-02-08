import requests
import pytest


def test_get_tracks_by_id():
    id_input = 1
    response = requests.get(f"http://backend:8080/tracks/{id_input}")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data
    assert "artist" in data
    assert "album" in data
    assert "genre" in data
    assert "duration" in data
