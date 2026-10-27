import logging as logger

from data.database_repository import get_database_client
from data.entity_service import EntityService
from utils.logger import get_logger

logger = get_logger(__name__)


class NonprofitService:
    def __init__(self, entity_service: EntityService):
        self.client = get_database_client()
        self.entity_service = entity_service

    async def get_nonprofits(self, page_number: int = 1, page_size: int = 4):
        """
        get nonprofits from database. Handles pagination.
        :param page_number: the page number to fetch
        :param page_size: the number of items per page
        :return: list of nonprofits
        """
        try:
            response = (
                self.client.table("nonprofits")
                .select("*")
                .range((page_number - 1) * page_size, page_number * page_size - 1)
                .execute()
            )
            if not response.data:
                logger.error(f"Error getting all nonprofits: {response}")
                return None
            entities = []
            for nonprofit in response.data:
                entity = await self.entity_service.get_entity_by_nonprofit_id(
                    nonprofit["id"]
                )
                if entity:
                    entities.append(entity[0])
                    # add nonprofit_id to entity data
                    entities[-1]["nonprofit_id"] = nonprofit["id"]

            return entities
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error getting all nonprofits: {e}")
            return None
