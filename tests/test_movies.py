from fastapi import status
from fastapi.testclient import TestClient

from app.const import (
    MOVIES_URL,
    MOVIES_URL_NEW,
)
from app.main import app


client = TestClient(app)


def test_get_movie(headers):
    params = {
        "movie_id": 1,
    }

    response = client.get("/" + MOVIES_URL, headers=headers, params=params)
    schema = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert schema["movie_id"] == 1


def test_get_movies(headers):
    params = {
        "year": 2000,
        "rating": 8,
    }

    url = "/" + MOVIES_URL + "/" + MOVIES_URL_NEW
    response = client.get(url, headers=headers, params=params)
    schema = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(schema) > 0
