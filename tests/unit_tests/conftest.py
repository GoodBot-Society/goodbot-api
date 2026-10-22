from unittest.mock import MagicMock, patch

import pytest

from data.database_repository import DatabaseRepository
from data.entity_service import EntityService
from data.expert_service import ExpertService
from data.home_service import HomeService
from data.litigation_service import LitigationService
from data.nonprofit_service import NonprofitService
from data.search_service import SearchService


@pytest.fixture
def repository():
    with patch("data.database_repository.get_database_client") as mock_client:
        mock_client.return_value = MagicMock()
        yield DatabaseRepository()


@pytest.fixture
def litigation_service():
    with patch("data.litigation_service.get_database_client") as mock_client:
        mock_client.return_value = MagicMock()
        yield LitigationService()


@pytest.fixture
def expert_service():
    with patch("data.expert_service.get_database_client") as mock_client:
        mock_client.return_value = MagicMock()
        yield ExpertService()


@pytest.fixture
def entity_service():
    with patch("data.entity_service.get_database_client") as mock_client:
        mock_client.return_value = MagicMock()
        yield EntityService()


@pytest.fixture
def nonprofit_service(entity_service):
    with patch("data.nonprofit_service.get_database_client") as mock_client:
        mock_client.return_value = MagicMock()
        yield NonprofitService(entity_service=entity_service)


@pytest.fixture
def search_service():
    with patch("data.search_service.get_database_client") as mock_client:
        mock_client.return_value = MagicMock()
        yield SearchService()


@pytest.fixture
def home_service():
    with patch("data.home_service.get_database_client") as mock_client:
        mock_client.return_value = MagicMock()
        yield HomeService()
