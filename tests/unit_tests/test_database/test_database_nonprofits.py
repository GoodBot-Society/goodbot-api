from unittest.mock import AsyncMock, MagicMock

import pytest


class TestDatabaseNonprofitsRepository:
    @pytest.mark.asyncio
    async def test_get_nonprofits(self, nonprofit_service, entity_service):
        response = MagicMock()
        response.data = [{"id": "np1"}, {"id": "np2"}]
        nonprofit_service.client.table.return_value.select.return_value.range.return_value.execute.return_value = (
            response
        )

        entity_service.get_entity_by_nonprofit_id = AsyncMock(
            side_effect=[
                [{"id": "entity1"}],
                [{"id": "entity2"}],
            ]
        )

        result = await nonprofit_service.get_nonprofits(1, 2)

        assert result == [
            {"id": "entity1", "nonprofit_id": "np1"},
            {"id": "entity2", "nonprofit_id": "np2"},
        ]

    @pytest.mark.asyncio
    async def test_get_nonprofits_no_data(self, nonprofit_service):
        response = MagicMock()
        response.data = []
        nonprofit_service.client.table.return_value.select.return_value.range.return_value.execute.return_value = (
            response
        )

        assert await nonprofit_service.get_nonprofits() is None

    @pytest.mark.asyncio
    async def test_get_nonprofits_exception(self, nonprofit_service):
        nonprofit_service.client.table.side_effect = Exception("DB error")

        assert await nonprofit_service.get_nonprofits() is None
