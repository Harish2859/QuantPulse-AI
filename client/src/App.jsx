import { useState } from 'react';
import { Activity, BrainCircuit, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';
import './App.css';

function App() {
  const [ticker, setTicker] = useState('');
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [logs, setLogs] = useState([]);

  const fetchAnalysis = () => {
    if (!ticker.trim()) {
      setError('Please enter a ticker symbol.');
      return;
    }

    setLoading(true);
    setError('');
    setReport(null);
    setLogs([]);

    const eventSource = new EventSource(`http://127.0.0.1:8000/analyze-stream?ticker=${ticker.toUpperCase()}`);

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.message) {
        setLogs((prev) => [...prev, data.message]);
      }

      if (data.status === 'complete') {
        const payload = data.report?.news_data?.[0] ?? data.report;
        setReport(payload ?? null);
        setLoading(false);
        eventSource.close();
      }

      if (data.status === 'error') {
        setError(data.message || 'The analysis request failed.');
        setLoading(false);
        eventSource.close();
      }
    };

    eventSource.onerror = () => {
      setError('The stream disconnected. Please try again.');
      setLoading(false);
      eventSource.close();
    };
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
        {loading || logs.length > 0 ? (
          <div className="report-card">
            <div className="report-header">
              <Sparkles size={18} />
              <h2>Agent reasoning log</h2>
            </div>
            <div className="log-window">
              {logs.map((entry, index) => (
                <div key={`${entry}-${index}`} className="log-line">
                  <span>$</span>
                  <p>{entry}</p>
                </div>
              ))}
              {loading && logs.length === 0 ? (
                <div className="log-line">
                  <span>$</span>
                  <p>Waiting for the workflow to begin...</p>
                </div>
              ) : null}
            </div>
          </div>
        ) : null}

        {!loading && report ? (
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
