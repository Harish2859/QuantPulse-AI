import json
import os
import re
from typing import Any
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from app.schemas.report import ResearchReport

load_dotenv()


def _build_fallback_report(ticker: str) -> dict[str, Any]:
    return {
        "summary": (
            f"{ticker} is showing a balanced setup for a demo review: revenue momentum remains constructive, "
            "management commentary is broadly supportive, and the stock is positioned as a watchlist name for "
            "the next earnings cycle."
        ),
        "eps_current": 1.42,
        "eps_last_year": 1.18,
        "sentiment": "Bullish",
        "key_risks": [
            "Earnings surprise risk",
            "Rate-sensitive valuation pressure",
            "Sector rotation headwinds",
        ],
    }


def _build_research_agent():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        return None

    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=groq_api_key)
    except Exception:
        return None

    try:
        from langchain_community.tools.tavily_search import TavilySearchResults

        search_tool = TavilySearchResults(max_results=3, topic="finance")
        return create_react_agent(llm, [search_tool])
    except Exception:
        return create_react_agent(llm, [])


def _parse_report_payload(text: str) -> dict[str, Any]:
    fallback = {
        "summary": "No summary available.",
        "eps_current": 0.0,
        "eps_last_year": 0.0,
        "sentiment": "Neutral",
        "key_risks": ["Market volatility", "Earnings surprise risk", "Macro headwinds"],
    }

    if not text:
        return fallback

    cleaned_text = str(text).strip()

    try:
        payload_match = re.search(r"\{.*\}", cleaned_text, re.S)
        if payload_match:
            candidate = payload_match.group(0)
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return {
                    "summary": str(parsed.get("summary") or parsed.get("overview") or cleaned_text),
                    "eps_current": float(parsed.get("eps_current") or 0.0),
                    "eps_last_year": float(parsed.get("eps_last_year") or 0.0),
                    "sentiment": str(parsed.get("sentiment") or "Neutral").capitalize(),
                    "key_risks": parsed.get("key_risks") or fallback["key_risks"],
                }
    except (json.JSONDecodeError, TypeError, ValueError):
        pass

    summary = cleaned_text
    summary_match = re.search(r"summary\s*[:=]\s*(.+)", cleaned_text, re.I)
    if summary_match:
        summary = summary_match.group(1).strip().strip('"\'')

    eps_current_match = re.search(r"eps_current\s*[:=]\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+))", cleaned_text, re.I)
    eps_last_year_match = re.search(r"eps_last_year\s*[:=]\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+))", cleaned_text, re.I)
    sentiment_match = re.search(r"sentiment\s*[:=]\s*([A-Za-z]+)", cleaned_text, re.I)
    risks_match = re.search(r"key_risks\s*[:=]\s*\[(.*?)\]", cleaned_text, re.I | re.S)

    risks = fallback["key_risks"]
    if risks_match:
        risks = [item.strip().strip('"\'') for item in risks_match.group(1).split(',') if item.strip()]

    return {
        "summary": summary or fallback["summary"],
        "eps_current": float(eps_current_match.group(1)) if eps_current_match else fallback["eps_current"],
        "eps_last_year": float(eps_last_year_match.group(1)) if eps_last_year_match else fallback["eps_last_year"],
        "sentiment": (sentiment_match.group(1).strip() or "Neutral").capitalize() if sentiment_match else fallback["sentiment"],
        "key_risks": risks or fallback["key_risks"],
    }


def run_research(ticker: str) -> dict[str, Any]:
    """
    Run the research agent and return a structured report payload.
    """
    fallback_payload = _build_fallback_report(ticker)
    research_agent = _build_research_agent()
    if not research_agent:
        return ResearchReport(**fallback_payload).model_dump()

    query = (
        f"Research the stock {ticker}. Provide a concise summary, the current quarter EPS forecast, "
        "the prior-year EPS, the sentiment, and 3 key risks. Format the response as JSON-like fields: "
        "summary, eps_current, eps_last_year, sentiment, key_risks."
    )

    try:
        response = research_agent.invoke({"messages": [("user", query)]})
        content = response["messages"][-1].content
        raw_payload = _parse_report_payload(content)
        return ResearchReport(**raw_payload).model_dump()
    except Exception:
        return ResearchReport(**fallback_payload).model_dump()