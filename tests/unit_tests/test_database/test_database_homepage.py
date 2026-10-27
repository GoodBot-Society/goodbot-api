from unittest.mock import MagicMock

import pytest


class TestDatabaseHomepageRepository:
    @pytest.mark.asyncio
    async def test_get_homepage_data(self, home_service):
        response = MagicMock()
        response.data = [{"id": 1}]
        home_service.client.rpc.return_value.execute.return_value = response

        result = await home_service.get_homepage_data()

        assert result == response.data
        home_service.client.rpc.assert_called_once_with("get_homepage_data2")

    @pytest.mark.asyncio
    async def test_get_homepage_data_exception(self, home_service):
        home_service.client.rpc.side_effect = Exception("DB error")

        assert await home_service.get_homepage_data() is None

    @pytest.mark.asyncio
    async def test_get_structural_subfactors(self, repository):
        response = MagicMock()
        response.data = [{"id": 1}]
        repository.client.table.return_value.select.return_value.execute.return_value = (
            response
        )

        assert await repository.get_structural_subfactors() == response.data

    @pytest.mark.asyncio
    async def test_get_structural_subfactors_exception(self, repository):
        repository.client.table.side_effect = Exception("DB error")

        assert await repository.get_structural_subfactors() is None
