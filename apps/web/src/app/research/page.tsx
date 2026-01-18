const bundles = [
  {
    id: "bundle-20240901",
    sharpe: 1.1,
    holdout: 0.9,
    status: "ready",
  },
];

export default function ResearchPage() {
  return (
    <main className="space-y-4">
      <header>
        <h2 className="page-title">Research Dashboard</h2>
        <p className="subtitle">
          Latest bundles and holdout results with AI promotion gates and calibration
          scores.
        </p>
      </header>
      <div className="two-column">
        <div className="card">
          {bundles.map((bundle) => (
            <div key={bundle.id} className="list-item">
              <div>
                <div className="page-title">{bundle.id}</div>
                <div className="subtitle">Status: {bundle.status}</div>
              </div>
              <div>
                <div className="subtitle">Sharpe {bundle.sharpe}</div>
                <div className="highlight">Holdout {bundle.holdout}</div>
              </div>
            </div>
          ))}
          <div className="actions">
            <button className="button primary">Select Bundle</button>
            <button className="button secondary">Promote Bundle</button>
          </div>
        </div>
        <div className="card">
          <h3>Promotion Gates</h3>
          <p>
            Holdout metrics must exceed baseline, worst fold performance must clear the
            minimum, and calibration quality must pass before live promotion.
          </p>
          <div className="section-grid">
            <div className="stat">
              <span>Holdout Sharpe</span>
              <h3>0.90</h3>
            </div>
            <div className="stat">
              <span>Max Drawdown</span>
              <h3>10%</h3>
            </div>
            <div className="stat">
              <span>Brier Score</span>
              <h3>0.12</h3>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
