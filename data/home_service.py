"""
This module contains the HomeService class, which provides methods to interact with the database and retrieve homepage data. The service uses a database client to execute stored procedures and handle exceptions, logging any errors encountered during the process.
"""

import logging as logger

from data.database_repository import get_database_client
from utils.logger import get_logger

logger = get_logger(__name__)


class HomeService:
    def __init__(self):
        self.client = get_database_client()

    async def get_homepage_data(self):
        """
        get homepage data through join queries from database
        """
        try:
            response = self.client.rpc("get_homepage_data").execute()
            return response.data
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error getting homepage data: {e}")
            return None
