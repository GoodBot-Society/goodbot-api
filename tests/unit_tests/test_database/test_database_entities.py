from unittest.mock import MagicMock

import pytest


class TestDatabaseEntities:
    @pytest.mark.asyncio
    async def test_get_entity_by_nonprofit_id(self, repository):
        response = MagicMock()
        response.data = [{"id": "np1", "entity_id": "entity1"}]
        repository.client.table.return_value.select.return_value.eq.return_value.execute.return_value = (
            response
        )

        assert await repository.get_entity_by_nonprofit_id("np1") == response.data

    @pytest.mark.asyncio
    async def test_get_entity_by_nonprofit_id_exception(self, repository):
        repository.client.table.side_effect = Exception("DB error")

        assert await repository.get_entity_by_nonprofit_id("np1") is None

    @pytest.mark.asyncio
    async def test_get_entity_by_id(self, repository):
        response = MagicMock()
        response.data = [{"id": "entity1"}]
        repository.client.table.return_value.select.return_value.eq.return_value.execute.return_value = (
            response
        )

        assert await repository.get_entity_by_id("entity1") == response.data

    @pytest.mark.asyncio
    async def test_get_entity_by_id_exception(self, repository):
        repository.client.table.side_effect = Exception("DB error")

        assert await repository.get_entity_by_id("entity1") is None

    @pytest.mark.asyncio
    async def test_get_entities_paginated(self, repository):
        response = MagicMock()
        response.data = [{"id": 1}]
        repository.client.table.return_value.select.return_value.range.return_value.execute.return_value = (
            response
        )

        result = await repository.get_entities(2, 4)

        assert result == response.data
        repository.client.table.return_value.select.return_value.range.assert_called_once_with(
            4, 7
        )

    @pytest.mark.asyncio
    async def test_get_entities_all(self, repository):
        response = MagicMock()
        response.data = [{"id": 1}]
        repository.client.table.return_value.select.return_value.execute.return_value = (
            response
        )

        assert await repository.get_entities(page_size=-1) == response.data

    @pytest.mark.asyncio
    async def test_get_entities_exception(self, repository):
        repository.client.table.side_effect = Exception("DB error")

        assert await repository.get_entities() is None

    @pytest.mark.asyncio
    async def test_update_entity_by_id(self, repository):
        response = MagicMock()
        response.data = [{"id": "entity1", "name": "Updated"}]
        repository.client.table.return_value.update.return_value.eq.return_value.execute.return_value = (
            response
        )

        result = await repository.update_entity_by_id("entity1", {"name": "Updated"})

        assert result == response.data

    @pytest.mark.asyncio
    async def test_update_entity_by_id_exception(self, repository):
        repository.client.table.side_effect = Exception("DB error")

        assert await repository.update_entity_by_id("entity1", {}) is None
