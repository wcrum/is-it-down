import os
import tempfile
import pytest
from main import create_app


@pytest.fixture
def client():
    app = create_app()

    with app.test_client() as client:
        yield client
