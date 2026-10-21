from unittest.mock import MagicMock

import pytest


class TestDatabaseSearch:
    @pytest.mark.asyncio
    async def test_search_by_keywords(self, repository):
        entity_response = MagicMock()
        entity_response.data = [{"id": "entity1"}]

        expert_response = MagicMock()
        expert_response.data = [{"id": "expert1"}]

        entity_search_response = MagicMock()
        entity_search_response.data = [{"id": "entity1"}]

        repository.client.from_.return_value.select.return_value.text_search.return_value.execute.return_value = (
            entity_response
        )
        repository.client.rpc.return_value.execute.side_effect = [
            expert_response,
            entity_search_response,
        ]

        nonprofit_response = MagicMock()
        nonprofit_response.data = [{"id": "np1", "entity_id": "entity1"}]

        repository.client.table.return_value.select.return_value.eq.return_value.execute.return_value = (
            nonprofit_response
        )

        result = await repository.search_by_keywords("education health")

        assert result == {
            "nonprofits": [{"id": "entity1"}],
            "experts": [{"id": "expert1"}],
        }

    @pytest.mark.asyncio
    async def test_search_by_keywords_removes_special_characters(self, repository):
        entity_response = MagicMock()
        entity_response.data = []

        expert_response = MagicMock()
        expert_response.data = []

        entity_search_response = MagicMock()
        entity_search_response.data = []

        repository.client.from_.return_value.select.return_value.text_search.return_value.execute.return_value = (
            entity_response
        )
        repository.client.rpc.return_value.execute.side_effect = [
            expert_response,
            entity_search_response,
        ]

        result = await repository.search_by_keywords("hello! @world#")

        assert result == {
            "nonprofits": [],
            "experts": [],
        }

    @pytest.mark.asyncio
    async def test_search_by_keywords_empty_after_sanitization(self, repository):
        result = await repository.search_by_keywords("!@#$%^&*()")

        assert result == {
            "nonprofits": [],
            "experts": [],
        }

    @pytest.mark.asyncio
    async def test_search_by_keywords_exception(self, repository):
        repository.client.from_.side_effect = Exception("DB error")

        assert await repository.search_by_keywords("test") is None
