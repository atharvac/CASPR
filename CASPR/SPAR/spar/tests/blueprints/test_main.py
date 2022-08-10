import pytest


def test_welcome_page_render(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"WYNKER" in response.data