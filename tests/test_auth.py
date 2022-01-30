from flask import request
from flask import current_app
from fixtures import client


def test_index(client):
    response = client.get("/auth/login", follow_redirects=True)

    assert request.base_url == current_app.config["UAA_AUTHORIZE_URI"]

    response = client.post(
        request.base_url,
        data={
            "username": "paul",
            "password": "wombat",
        },
        follow_redirects=True,
    )
