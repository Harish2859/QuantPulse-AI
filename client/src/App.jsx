import { useState } from 'react';
import axios from 'axios';
import { Activity, BrainCircuit, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';
import './App.css';

function App() {
  const [ticker, setTicker] = useState('');
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchAnalysis = async () => {
    if (!ticker.trim()) {
      setError('Please enter a ticker symbol.');
      return;
    }

    setLoading(true);
    setError('');
    setReport(null);

    try {
      const response = await axios.post('http://127.0.0.1:8000/analyze', { ticker: ticker.toUpperCase() });
      setReport(response.data?.data?.news_data?.[0] ?? null);
    } catch (err) {
      console.error('Error fetching analysis:', err);
      setError('The analysis request failed. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <motion.section
        className="hero-panel"
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
      >
        <div className="hero-copy">
          <div className="pill">
            <BrainCircuit size={16} />
            Agentic research workspace
          </div>
          <h1>QuantPulse AI</h1>
          <p>
            Ask the backend to analyze a stock, and let the LangGraph agent build a concise research report for you.
          </p>
        </div>

        <div className="control-card">
          <label htmlFor="ticker">Ticker Symbol</label>
          <div className="input-row">
            <input
              id="ticker"
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
              placeholder="e.g. AAPL"
            />
            <button onClick={fetchAnalysis} disabled={loading}>
              {loading ? 'Researching...' : 'Analyze'}
            </button>
          </div>

          {error ? <p className="error-text">{error}</p> : null}
        </div>
      </motion.section>

      <motion.section
        className="results-panel"
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.4 }}
      >
        {loading ? (
          <div className="loading-state">
            <Sparkles size={20} />
            <span>The agent is gathering market context and summarizing the latest signal.</span>
          </div>
        ) : report ? (
          <div className="report-card">
            <div className="report-header">
              <Activity size={18} />
              <h2>Structured research output</h2>
            </div>

            <div className="metrics-grid">
              <div className="metric-card">
                <span>EPS (current)</span>
                <strong>{report.eps_current}</strong>
              </div>
              <div className="metric-card">
                <span>EPS (last year)</span>
                <strong>{report.eps_last_year}</strong>
              </div>
              <div className="metric-card">
                <span>Sentiment</span>
                <strong>{report.sentiment}</strong>
              </div>
            </div>

            <div className="reasoning-card">
              <h3>Summary</h3>
              <p>{report.summary}</p>
            </div>

            <div className="reasoning-card">
              <h3>Key risks</h3>
              <ul>
                {report.key_risks?.map((risk) => (
                  <li key={risk}>{risk}</li>
                ))}
              </ul>
            </div>
          </div>
        ) : (
          <div className="empty-state">
            <p>Enter a ticker and start the analysis workflow.</p>
          </div>
        )}
      </motion.section>
    </div>
  );
}

export default App;
