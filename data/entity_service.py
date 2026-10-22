import logging as logger

from data.database_repository import get_database_client
from utils.logger import get_logger

logger = get_logger(__name__)


class EntityService:

    def __init__(self):
        self.client = get_database_client()

    async def get_entity_by_nonprofit_id(self, nonprofit_id: str):
        """
        get entity by given nonprofit id from database
        :param nonprofit_id: the id of the nonprofit
        :return: entity data or None if not found
        """
        try:
            print(f"Fetching entity by nonprofit id: {nonprofit_id}")
            response = (
                self.client.table("nonprofits")
                .select("entity_id")
                .eq("id", nonprofit_id)
                .execute()
            )
            if not response.data:
                logger.warning(f"Error getting entity by nonprofit id: {response}")
                return None
            entity_id = response.data[0]["entity_id"]
            response = (
                self.client.table("entities").select("*").eq("id", entity_id).execute()
            )
            return response.data
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error getting entity by nonprofit id: {e}")
            return None

    async def get_entity_by_id(self, entity_id: str):
        """
        get entity by given entity id from database
        :param entity_id: the id of the entity
        :return: entity data or None if not found
        """
        try:
            response = (
                self.client.table("entities").select("*").eq("id", entity_id).execute()
            )
            return response.data
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error getting entity by id: {e}")
            return None

    async def get_entities(self, page_number: int = 1, page_size: int = 4):
        """
        get entities from database. Handles pagination.
        :param page_number: the page number to fetch
        :param page_size: the number of items per page
        :return: list of entities
        """
        try:
            # if page_size is -1, fetch all entities
            if page_size == -1:
                response = self.client.table("entities").select("*").execute()
                return response.data
            response = (
                self.client.table("entities")
                .select("*")
                .range((page_number - 1) * page_size, page_number * page_size - 1)
                .execute()
            )
            return response.data
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error getting all entities: {e}")
            return None

    async def update_entity_by_id(self, entity_id: str, update_data: dict):
        """
        update entity by given entity id in database
        :param entity_id: the id of the entity
        :param update_data: the data to update
        :return: updated entity data or None if not found
        """
        try:
            response = (
                self.client.table("entities")
                .update(update_data)
                .eq("id", entity_id)
                .execute()
            )
            return response.data
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error updating entity by id: {e}")
            return None
