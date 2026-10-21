from unittest.mock import MagicMock


class TestDatabaseUsers:
    def test_user_exists_active_user(self, repository):
        response = MagicMock()
        response.data = [{"active": 1}]
        repository.client.table.return_value.select.return_value.eq.return_value.execute.return_value = (
            response
        )

        result = repository.user_exists("TestUser")

        assert result is True

    def test_user_exists_inactive_user(self, repository):
        response = MagicMock()
        response.data = [{"active": 0}]
        repository.client.table.return_value.select.return_value.eq.return_value.execute.return_value = (
            response
        )

        assert repository.user_exists("TestUser") is False

    def test_user_exists_user_not_found(self, repository):
        response = MagicMock()
        response.data = []
        repository.client.table.return_value.select.return_value.eq.return_value.execute.return_value = (
            response
        )

        assert repository.user_exists("TestUser") is False

    def test_user_exists_exception(self, repository):
        repository.client.table.side_effect = Exception("DB error")

        assert repository.user_exists("TestUser") is False

    def test_get_user_by_username(self, repository):
        response = MagicMock()
        response.data = [{"username": "testuser"}]
        repository.client.table.return_value.select.return_value.eq.return_value.execute.return_value = (
            response
        )

        result = repository.get_user_by_username("TestUser")

        assert result == {"username": "testuser"}

    def test_get_user_by_username_exception(self, repository):
        repository.client.table.side_effect = Exception("DB error")

        assert repository.get_user_by_username("TestUser") is None

    def test_insert_user(self, repository):
        response = MagicMock()
        response.data = [{"username": "testuser"}]
        repository.client.table.return_value.insert.return_value.execute.return_value = (
            response
        )

        result = repository.insert_user("TestUser", "hashed-password")

        assert result == response.data
        repository.client.table.return_value.insert.assert_called_once_with(
            {
                "username": "testuser",
                "password": "hashed-password",
            }
        )

    def test_insert_user_exception(self, repository):
        repository.client.table.side_effect = Exception("DB error")

        assert repository.insert_user("TestUser", "hash") is None
