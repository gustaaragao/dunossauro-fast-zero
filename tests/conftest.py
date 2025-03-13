import pytest
from fastapi.testclient import TestClient

from zero.app import app


@pytest.fixture
def client():
    return TestClient(app)
