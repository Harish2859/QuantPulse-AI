import os
import traceback
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatGroq(model='llama-3.3-70b-versatile', temperature=0, api_key=os.getenv('GROQ_API_KEY'))
search_tool = TavilySearchResults(max_results=3, topic='finance')
agent = create_react_agent(llm, [search_tool])

try:
    response = agent.invoke({'messages': [('user', 'Research AAPL and give a short summary.')]})
    print(response['messages'][-1].content)
except Exception:
    traceback.print_exc()
