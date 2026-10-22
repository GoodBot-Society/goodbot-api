from unittest.mock import MagicMock, patch

from data.database_repository import get_database_client


class TestGetDatabaseClient:
    def test_creates_database_client(self):
        get_database_client.cache_clear()

        with patch("data.database_repository.create_client") as mock_create:
            mock_create.return_value = MagicMock()

            result = get_database_client()

            mock_create.assert_called_once()
            assert result == mock_create.return_value

    def test_returns_cached_client(self):
        get_database_client.cache_clear()

        with patch("data.database_repository.create_client") as mock_create:
            mock_create.return_value = MagicMock()

            first = get_database_client()
            second = get_database_client()

            assert first is second
            mock_create.assert_called_once()
