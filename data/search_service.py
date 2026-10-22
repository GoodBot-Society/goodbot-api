"""
This module provides a SearchService class that allows searching for entities, nonprofits, and experts in a database based on given keywords. It sanitizes the input, performs full-text search, and returns the results in a structured format. The service handles exceptions and logs errors for better traceability.
"""

import logging as logger
import re

from data.database_repository import get_database_client
from utils.logger import get_logger

logger = get_logger(__name__)


class SearchService:
    def __init__(self):
        self.client = get_database_client()

    async def search_by_keywords(self, keywords: str):
        """
        search entities, nonprofits and experts by given keywords in database
        :param keywords: the keywords to search
        :return: list of entities, nonprofits and experts matching the keywords
        """
        try:
            # Sanitize input - remove special characters except alphanumeric, spaces, and hyphens
            keywords = re.sub(r"[^a-zA-Z0-9\s\-]", "", keywords)

            # Limit length to prevent DoS
            keywords = keywords[:500]

            # turn string keywords into an array or keywords
            keywords = keywords.replace(" ", ",")
            keywords_array = keywords.split(",")
            # Filter out empty strings
            keywords_array = [k.strip() for k in keywords_array if k.strip()]

            if not keywords_array:
                logger.warning("No valid keywords after sanitization")
                return {"nonprofits": [], "experts": []}

            # add single quotes (') around each keyword
            keywords_array = [f"'{keyword}'" for keyword in keywords_array]
            # join the keywords with | operator for full text search
            keywords = " | ".join(keywords_array)

            result_entities = (
                self.client.from_("entities")
                .select("id")
                .text_search("about", keywords)
                .execute()
            )

            result_experts = self.client.rpc(
                "search_experts_with_keyword", {"q": keywords}
            ).execute()

            # get nonprofits by entity ids
            result_nonprofits = []
            for entity in result_entities.data:
                nonprofits = (
                    self.client.table("nonprofits")
                    .select("*")
                    .eq("entity_id", entity["id"])
                    .execute()
                )
                if nonprofits.data:
                    result_nonprofits.extend(nonprofits.data)

            # filter result_entities to only include those with matching nonprofits
            result_entities.data = [
                entity
                for entity in result_entities.data
                if any(
                    nonprofit["entity_id"] == entity["id"]
                    for nonprofit in result_nonprofits
                )
            ]

            result_entities = self.client.rpc(
                "search_entities_with_keyword", {"q": keywords}
            ).execute()

            # combine results into a json object
            response = {
                "nonprofits": result_entities.data,
                "experts": result_experts.data,
            }
            return response
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error searching by keywords: {e}")
            return None
