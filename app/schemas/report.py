from pydantic import BaseModel


class PersonalityReport(BaseModel):
    summary: str
    core_traits: list[str]
    strengths: list[str]
    growth_areas: list[str]
    career_style: str
    relationship_style: str
    confidence_note: str
    disclaimer: str