"""
This module contains the LitigationService class which provides methods to interact with the litigation data in the database.
"""

import logging as logger

from data.database_repository import get_database_client
from model.litigations_response_v1 import LitigationResponse
from utils.logger import get_logger

logger = get_logger(__name__)


class LitigationService:
    def __init__(self):
        self.client = get_database_client()

    def parse_litigation_response(self, data: dict) -> LitigationResponse:
        """
        parse litigation response from database to LitigationResponse model
        """
        return LitigationResponse(
            id=data["id"],
            case_number=data["case_number"],
            year=data["year"],
            status=data.get("status"),
            decision=data.get("decision"),
            decision_date=data.get("decision_date"),
            jurisdiction=data.get("jurisdiction"),
            sub_jurisdictions=data.get("sub_jurisdictions", []),
            plaintiffs=data.get("plaintiffs", []),
            plaintiff_categories=data.get("plaintiff_categories", []),
            plaintiff_types=data.get("plaintiff_types", []),
            imp_groups=data.get("imp_groups", []),
            respondent_types=data.get("respondent_types", []),
            respondent_categories=data.get("respondent_categories", []),
            respondents=data.get("respondents", []),
            harm_risks=data.get("harm_risks", []),
            law_areas=data.get("law_areas", []),
            outcome_notes=data.get("outcome_notes"),
            links=data.get("links", []),
            court_level=data.get("court_level"),
        )

    def get_litigations(self) -> list[LitigationResponse] | None:
        """
        get all litigations from database
        """
        try:
            response = self.client.rpc("get_litigations").execute()
            parsed_response = [
                self.parse_litigation_response(item) for item in response.data
            ]
            return parsed_response
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error getting all litigations: {e}")
            return None

    def get_litigation_by_id(self, litigation_id: str) -> LitigationResponse | None:
        """
        get litigation by given litigation id from database
        :param litigation_id: the id of the litigation
        :return: litigation data or None if not found
        """

        try:
            response = self.client.rpc(
                "get_litigations", {"litigation_id": litigation_id}
            ).execute()
            if not response.data:
                logger.warning(f"Litigation with id {litigation_id} not found")
                return None
            parsed_response = self.parse_litigation_response(response.data[0])
            return parsed_response
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error getting litigation by id: {e}")
            return None
