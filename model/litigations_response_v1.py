from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class LitigationResponse(BaseModel):
    id: str
    case_number: str
    year: int

    status: str | None = None
    decision: str | None = None
    decision_date: datetime | None = None

    jurisdiction: str | None = None
    sub_jurisdictions: list[str]
    plaintiffs: list[str]
    plaintiff_categories: list[str]
    plaintiff_types: list[str]

    imp_groups: list[str]
    respondent_types: list[str]
    respondent_categories: list[str]
    respondents: list[str]

    harm_risks: list[str]
    law_areas: list[str]

    outcome_notes: str | None = None
    links: list[str]
    court_level: str | None = None
