import pytest
from starlette.testclient import TestClient
from src import create_app


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    client = TestClient(app)
    yield client