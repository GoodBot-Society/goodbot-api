"""
Unit tests for Litigation endpoints.
"""

from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.main import app
from routes.litigations_route_v1 import get_database_repository


@pytest.fixture
def mock_repo() -> MagicMock:
    repo = MagicMock()
    repo.get_litigations.return_value = [
        {
            "id": "l1",
            "case_number": "CN123",
            "year": 2023,
        }
    ]
    repo.get_litigation_by_id.return_value = {
        "id": "l1",
        "case_number": "CN123",
        "year": 2023,
    }
    return repo


@pytest.fixture
def client(mock_repo):
    app.dependency_overrides[get_database_repository] = lambda: mock_repo
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}


def test_get_litigations_success(client, mock_repo):
    response = client.get("/v1/litigations/")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == "l1"


def test_get_litigations_empty(client, mock_repo):
    mock_repo.get_litigations.return_value = None
    response = client.get("/v1/litigations/")
    assert response.status_code == 404
    assert response.json()["detail"] == "No litigations found"


def test_get_litigations_error(client, mock_repo):
    mock_repo.get_litigations.side_effect = Exception("DB error")
    response = client.get("/v1/litigations/")
    assert response.status_code == 500
    assert response.json()["detail"] == "Error fetching litigations"


def test_get_litigation_by_id_success(client, mock_repo):
    response = client.get("/v1/litigations/l1")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["id"] == "l1"


def test_get_litigation_by_id_not_found(client, mock_repo):
    mock_repo.get_litigation_by_id.return_value = None
    response = client.get("/v1/litigations/unknown")
    assert response.status_code == 404
    assert response.json()["detail"] == "Litigation with ID unknown not found"


def test_get_litigation_by_id_error(client, mock_repo):
    mock_repo.get_litigation_by_id.side_effect = Exception("DB error")
    response = client.get("/v1/litigations/l1")
    assert response.status_code == 500
    assert response.json()["detail"] == "Error fetching litigation with ID l1"
