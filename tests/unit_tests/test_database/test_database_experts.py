from unittest.mock import MagicMock

import pytest


class TestDatabaseExperts:
    @pytest.mark.asyncio
    async def test_get_experts_paginated(self, repository):
        response = MagicMock()
        response.data = [{"id": 1}]
        repository.client.table.return_value.select.return_value.range.return_value.execute.return_value = (
            response
        )

        result = await repository.get_experts(page_number=2, page_size=10)

        assert result == response.data
        repository.client.table.return_value.select.return_value.range.assert_called_once_with(
            10, 19
        )

    @pytest.mark.asyncio
    async def test_get_experts_all(self, repository):
        response = MagicMock()
        response.data = [{"id": 1}]
        repository.client.table.return_value.select.return_value.execute.return_value = (
            response
        )

        result = await repository.get_experts(page_size=-1)

        assert result == response.data

    @pytest.mark.asyncio
    async def test_get_experts_exception(self, repository):
        repository.client.table.side_effect = Exception("DB error")

        assert await repository.get_experts() is None

    @pytest.mark.asyncio
    async def test_get_expert_by_id(self, repository):
        response = MagicMock()
        response.data = [{"id": "123"}]
        repository.client.table.return_value.select.return_value.eq.return_value.execute.return_value = (
            response
        )

        assert await repository.get_expert_by_id("123") == response.data

    @pytest.mark.asyncio
    async def test_get_expert_by_id_exception(self, repository):
        repository.client.table.side_effect = Exception("DB error")

        assert await repository.get_expert_by_id("123") is None

    @pytest.mark.asyncio
    async def test_update_expert_by_id(self, repository):
        response = MagicMock()
        response.data = [{"id": "123", "name": "Updated"}]
        repository.client.table.return_value.update.return_value.eq.return_value.execute.return_value = (
            response
        )

        result = await repository.update_expert_by_id("123", {"name": "Updated"})

        assert result == response.data

    @pytest.mark.asyncio
    async def test_update_expert_by_id_exception(self, repository):
        repository.client.table.side_effect = Exception("DB error")

        assert await repository.update_expert_by_id("123", {}) is None
