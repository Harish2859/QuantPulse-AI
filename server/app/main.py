from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.graph import app as research_graph # Absolute import from the 'app' package

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    ticker: str

@api.post("/analyze")
async def analyze_stock(request: ResearchRequest):
    initial_state = {"ticker": request.ticker}
    result = await research_graph.ainvoke(initial_state)
    return {"status": "success", "data": result}