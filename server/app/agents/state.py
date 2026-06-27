from typing import TypedDict, List
from app.schemas.report import ResearchReport

class AgentState(TypedDict):
    ticker: str
    raw_transcript: str
    news_data: List[str]
    report: ResearchReport