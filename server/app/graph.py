from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.researcher import run_research

# Define the node function
def research_node(state: AgentState):
    ticker = state["ticker"]
    print(f"--- RESEARCHING {ticker} ---")
    research_results = run_research(ticker)
    return {"news_data": [research_results]}

# Build the workflow
workflow = StateGraph(AgentState)
workflow.add_node("researcher", research_node)
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", END)

# Compile the graph
app = workflow.compile()