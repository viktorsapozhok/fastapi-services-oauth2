from fastapi import status
from fastapi.testclient import TestClient

from app.const import (
    AUTH_URL,
    TOKEN_TYPE,
)
from app.main import app


client = TestClient(app)


def test_login(config):
    data = {
        "username": config.username,
        "password": config.password,
    }

    response = client.post("/" + AUTH_URL, data=data)
    schema = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert schema["token_type"] == TOKEN_TYPE
    assert isinstance(schema["access_token"], str)


def test_incorrect_password(config):
    data = {
        "username": config.username,
        "password": "fake_password",
    }

    response = client.post("/" + AUTH_URL, data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
