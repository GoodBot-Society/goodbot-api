"""Tests for Search by keywords endpoint."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from api.main import app
from routes.search_route_v1 import get_search_service


class TestSearch:
    """Test suite for the Search by keywords endpoint."""

    @pytest.fixture
    def mock_repo(self):
        """Create a mock SearchService for dependency override.

        The only method used by the route is ``search_by_keywords`` and
        it is asynchronous, so we stub it with ``AsyncMock``.
        """
        mock = MagicMock()
        mock.search_by_keywords = AsyncMock()
        return mock

    @pytest.fixture
    def client(self, mock_repo):
        """Override the SearchService dependency for the FastAPI app.

        The override is reset after each test to avoid leaking state
        between tests.
        """
        app.dependency_overrides[get_search_service] = lambda: mock_repo
        test_client = TestClient(app)
        yield test_client
        app.dependency_overrides = {}

    def test_search(self, client, mock_repo):
        """Test that /search/{keywords} returns search results."""
        # Arrange
        expected = {
            "nonprofits": [{"id": "np1"}],
            "experts": [{"id": "e1"}],
        }
        mock_repo.search_by_keywords.return_value = expected

        # Act
        response = client.get("/v1/search/education")

        # Assert
        assert response.status_code == 200
        assert response.json() == expected

    def test_search_no_results(self, client, mock_repo):
        """Test that /search/{keywords} returns no results when service returns None."""
        mock_repo.search_by_keywords.return_value = None

        response = client.get("/v1/search/invalidterm")

        assert response.status_code == 200
        body = response.json()
        assert body["nonprofits"] == []
        assert body["experts"] == []
        assert body["query"] == "invalidterm"

    def test_search_error(self, client, mock_repo):
        """Test that /search/{keywords} returns 500 on a DB error."""
        mock_repo.search_by_keywords.side_effect = Exception("DB error")

        response = client.get("/v1/search/foo")

        assert response.status_code == 500
