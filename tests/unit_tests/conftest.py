from unittest.mock import MagicMock, patch

import pytest

from data.database_repository import DatabaseRepository


@pytest.fixture
def repository():
    with patch("data.database_repository.get_database_client") as mock_client:
        mock_client.return_value = MagicMock()
        yield DatabaseRepository()
