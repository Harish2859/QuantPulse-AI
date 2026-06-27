# QuantPulse AI 🚀
*Autonomous Financial Research & Sentiment Intelligence*

QuantPulse AI is an agentic financial research engine that automates the analysis of real-time market data, earnings transcripts, and financial sentiment. By leveraging **LangGraph** for orchestrating complex research workflows and **FastAPI** for low-latency delivery, it provides institutional-grade investment summaries in seconds.

## 🏗️ Architecture Overview
QuantPulse AI moves beyond standard RAG (Retrieval-Augmented Generation) by implementing a multi-step agentic workflow:

1. **Orchestration Layer:** Built with LangGraph, managing the state machine of the research pipeline.
2. **Research Engine:** Autonomous scraping and search via Tavily and Firecrawl.
3. **Intelligence Layer:** Groq (Llama-3.3) for high-speed reasoning and structured data extraction.
4. **Frontend:** React-based dashboard featuring a real-time "Agent Reasoning Log."

## 🛠️ Tech Stack

- **Orchestration:** LangGraph (Python)
- **API:** FastAPI (Asynchronous Event Streaming)
- **Frontend:** React.js, Tailwind CSS, Framer Motion
- **AI Engine:** Llama-3.3 (via Groq)
- **Data Sources:** Tavily (Real-time Market Data)

## 🚀 Key Features

- **Streaming Reasoning:** Real-time visibility into the agent's thought process (Agentic Log).
- **Structured Extraction:** Pydantic-enforced schema validation ensures consistent financial metrics (EPS, Sentiment, etc.).
- **Asynchronous Pipeline:** Non-blocking API calls for improved scalability.
- **Error Resilience:** Robust retry logic and state management built into the LangGraph workflow.

## ⚙️ Installation

### Prerequisites

- Python 3.12+
- Node.js 18+
- API Keys: [Groq](https://console.groq.com/) & [Tavily](https://tavily.com/)

### Backend Setup

```bash
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
# Create a .env file with your API keys
python -m uvicorn app.main:api --reload
```

### Frontend Setup

```bash
cd client
npm install
npm run dev
```

## 💡 Why QuantPulse?
Most AI research tools treat the LLM as a chatbot. QuantPulse treats the LLM as an **Autonomous Analyst**. By explicitly modeling the "Research Flow" as a directed graph, we reduce hallucinations, increase precision, and provide users with a transparent audit trail of how the research was gathered.

## 👤 Author
**Harish M.**

- *B.Tech in Artificial Intelligence & Data Science*
- [GitHub](https://github.com/Harish2859) | [Portfolio/LinkedIn Link]

## 🔮 Future Roadmap

- Add interactive stock price charts and financial visualizations.
- Support PDF and earnings transcript uploads for deeper document analysis.
- Expand the agent workflow to include multi-asset research and portfolio monitoring.
