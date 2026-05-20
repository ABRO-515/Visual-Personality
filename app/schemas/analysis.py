from pydantic import BaseModel
from typing import Any


class AnalysisResponse(BaseModel):
    type: str
    quality: dict[str, Any]
    features: dict[str, Any]
    traits: list[str]
