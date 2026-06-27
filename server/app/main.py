import asyncio
import json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.graph import app as research_graph

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    ticker: str


async def stream_agent_steps(ticker: str):
    initial_state = {"ticker": ticker}
    steps = [
        f"Initializing workflow for {ticker}...",
        "Gathering market context...",
        "Analyzing recent signals...",
        "Synthesizing research summary...",
    ]

    for step in steps:
        yield f"data: {json.dumps({'status': 'running', 'message': step})}\n\n"
        await asyncio.sleep(0.35)

    try:
        result = await research_graph.ainvoke(initial_state)
        payload = json.dumps({"status": "complete", "message": "Analysis complete", "report": result})
    except Exception as exc:
        payload = json.dumps({"status": "error", "message": str(exc)})

    yield f"data: {payload}\n\n"


@api.post("/analyze")
async def analyze_stock(request: ResearchRequest):
    initial_state = {"ticker": request.ticker}
    result = await research_graph.ainvoke(initial_state)
    return {"status": "success", "data": result}


@api.get("/analyze-stream")
async def analyze_stream(ticker: str = Query(...)):
    return StreamingResponse(stream_agent_steps(ticker), media_type="text/event-stream")