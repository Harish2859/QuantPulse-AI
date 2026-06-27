from pydantic import BaseModel, Field
from typing import List

class ResearchReport(BaseModel):
    summary: str = Field(description="A concise 3-4 sentence overview")
    eps_current: float = Field(description="The current quarter consensus EPS forecast")
    eps_last_year: float = Field(description="The reported EPS for the same quarter last year")
    sentiment: str = Field(description="Bullish, Bearish, or Neutral sentiment")
    key_risks: List[str] = Field(description="List of 3 primary risks for the stock")