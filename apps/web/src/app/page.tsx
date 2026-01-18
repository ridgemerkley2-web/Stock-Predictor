const cards = [
  {
    title: "Scanner Status",
    description: "Universe refresh every 60 minutes, 1-min scans with 5m bars.",
  },
  {
    title: "Signals",
    description: "Momentum, mean reversion, and volatility breakout ensemble.",
  },
  {
    title: "Execution",
    description: "Bracket orders, idempotent placement, and circuit breakers.",
  },
  {
    title: "Research",
    description: "Walk-forward optimization with blind holdout promotion gates.",
  },
];

export default function HomePage() {
  return (
    <main className="space-y-6">
      <div className="status-row">
        <span className="status-pill">AI Mesh: Online</span>
        <span className="status-pill">Neural Links: Synced</span>
        <span className="status-pill">Latency: 42ms</span>
        <span className="status-pill">Regime: Risk-On</span>
      </div>
      <section className="hero">
        <h2>Neural Trade Command</h2>
        <p>
          AI-driven signal routing, deep learning calibration, and real-time execution
          are orchestrated from this command bridge.
        </p>
        <div className="button-row">
          <button className="button primary">Enable Live Trading</button>
          <button className="button secondary">Flatten All</button>
        </div>
      </section>

      <section className="terminal-grid">
        <div>
          <div className="section-grid">
            {cards.map((card) => (
              <div key={card.title} className="card">
                <h3>{card.title}</h3>
                <p>{card.description}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="ai-panel">
          <h4>Neural AI Core</h4>
          <div className="ai-flow">
            <span>
              Model Stack <strong>Transformer + TFT</strong>
            </span>
            <span>
              Calibration <strong>Isotonic v3</strong>
            </span>
            <span>
              Confidence Gate <strong>0.67</strong>
            </span>
            <span>
              Execution Bias <strong>Long-Only</strong>
            </span>
          </div>
          <div className="chip-grid">
            <div className="chip">Signal Health: 97%</div>
            <div className="chip">Regime Sync: ✅</div>
            <div className="chip">Risk Dampener: On</div>
            <div className="chip">Edge Filter: Active</div>
          </div>
          <div className="link-list">
            <span>Neural Link A</span>
            <span>Neural Link B</span>
            <span>Deep Learning Core</span>
            <span>Strategy Mesh</span>
          </div>
        </div>
      </section>
    </main>
  );
}
