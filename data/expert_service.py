import logging as logger

from data.database_repository import get_database_client
from utils.logger import get_logger

logger = get_logger(__name__)


class ExpertService:
    def __init__(self):
        self.client = get_database_client()

    async def get_experts(self, page_number: int = 1, page_size: int = 10):
        """
        get experts from database. Handles pagination.
        :param page_number: the page number to fetch
        :param page_size: the number of items per page
        :return: list of experts
        """
        try:
            # if page_size is -1, fetch all experts
            if page_size == -1:
                response = self.client.table("experts").select("*").execute()
                return response.data
            response = (
                self.client.table("experts")
                .select("*")
                .range((page_number - 1) * page_size, page_number * page_size - 1)
                .execute()
            )
            return response.data
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error getting all experts: {e}")
            return None

    async def get_expert_by_id(self, expert_id: str):
        """
        get expert by given expert id from database
        :param expert_id: the id of the expert
        :return: expert data or None if not found
        """
        try:
            response = (
                self.client.table("experts").select("*").eq("id", expert_id).execute()
            )
            return response.data
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error getting expert by id: {e}")
            return None

    async def update_expert_by_id(self, expert_id: str, update_data: dict):
        """
        update expert by given expert id in database
        :param expert_id: the id of the expert
        :param update_data: the data to update
        :return: updated expert data or None if not found
        """
        try:
            response = (
                self.client.table("experts")
                .update(update_data)
                .eq("id", expert_id)
                .execute()
            )
            return response.data
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error updating expert by id: {e}")
            return None
