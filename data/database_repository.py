"""
database operations module
"""

from functools import lru_cache

from supabase import Client, create_client

from config import get_settings
from utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


@lru_cache(maxsize=1)
def get_database_client() -> Client:
    """
    create supabase client using environment variables
    Uses lru_cache to ensure we only create one client instance
    """
    logger.info("Creating Supabase client")
    client: Client = create_client(settings.database_url, settings.database_api_key)
    return client


class DatabaseRepository:
    """
    repository class for database operations.
    This class encapsulates the database operations and provides methods to interact with the database.
    """

    def __init__(self):
        self.client = get_database_client()

    def user_exists(self, value: str):
        """
        check if user exists in database
        """
        try:
            response = (
                self.client.table("users")
                .select("*")
                .eq("username", value.lower())
                .execute()
            )
            return len(response.data) > 0 and response.data[0]["active"] == 1
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error checking if user exists: {e}")
            return False

    def get_user_by_username(self, username: str):
        """
        get user from database by username
        """
        try:
            response = (
                self.client.table("users")
                .select("*")
                .eq("username", username.lower())
                .execute()
            )
            return response.data[0]
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error getting user by username: {e}")
            return None

    def insert_user(self, username: str, hashed_password: str):
        """
        inserts new user into database
        """
        try:
            response = (
                self.client.table("users")
                .insert({"username": username.lower(), "password": hashed_password})
                .execute()
            )
            return response.data
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error inserting user into database: {e}")
            return None

    async def get_structural_subfactors(self):
        """
        get all structural subfactors from database
        """
        try:
            response = self.client.table("structural_sub_factors").select("*").execute()
            return response.data
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error getting all structural subfactors: {e}")
            return None
