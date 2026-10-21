from unittest.mock import MagicMock


class TestLitigationRepository:
    def test_get_litigations_success(self, repository):
        """Returns parsed litigations when the RPC succeeds."""
        response = MagicMock()
        response.data = [{"id": "123", "case_number": "2024-001", "year": 2024}]

        repository.client.rpc.return_value.execute.return_value = response

        result = repository.get_litigations()

        assert len(result) == 1
        assert result[0].case_number == "2024-001"
        repository.client.rpc.assert_called_once_with("get_litigations")

    def test_get_litigations_empty(self, repository):
        response = MagicMock()
        response.data = []

        repository.client.rpc.return_value.execute.return_value = response

        result = repository.get_litigations()

        assert result == []

    def test_get_litigations_failure(self, repository):
        repository.client.rpc.side_effect = Exception("DB error")

        result = repository.get_litigations()

        assert result is None

    def test_get_litigation_by_id_success(self, repository):
        litigation_id = "123"
        litigation = {
            "id": litigation_id,
            "case_number": "2024-001",
            "year": 2024,
        }
        response = MagicMock()
        response.data = [litigation]
        repository.client.rpc.return_value.execute.return_value = response

        result = repository.get_litigation_by_id(litigation_id)

        assert result is not None
        assert result.case_number == "2024-001"
        repository.client.rpc.assert_called_once_with(
            "get_litigations", {"litigation_id": litigation_id}
        )

    def test_get_litigation_by_id_not_found(self, repository):
        response = MagicMock()
        response.data = []
        repository.client.rpc.return_value.execute.return_value = response

        result = repository.get_litigation_by_id("nonexistent-id")

        assert result is None

    def test_get_litigation_by_id_failure(self, repository):
        repository.client.rpc.side_effect = Exception("DB error")

        result = repository.get_litigation_by_id("123")

        assert result is None
