const rows = [
  {
    ticker: "AAPL",
    ev: 0.42,
    certainty: 0.78,
    entry: 197.4,
    stop: 193.2,
    target: 207.8,
  },
  {
    ticker: "NVDA",
    ev: 0.37,
    certainty: 0.71,
    entry: 122.8,
    stop: 118.9,
    target: 131.4,
  },
];

export default function BestBuysPage() {
  return (
    <main className="space-y-4">
      <header>
        <h2 className="page-title">Best Buys Now</h2>
        <p className="subtitle">
          AI-ranked candidates with neural confidence scoring and transformer-confirmed
          momentum.
        </p>
      </header>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Ticker</th>
              <th>EV</th>
              <th>Certainty</th>
              <th>Entry</th>
              <th>Stop</th>
              <th>Target</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.ticker}>
                <td>
                  <span className="pill">{row.ticker}</span>
                </td>
                <td>{row.ev.toFixed(2)}</td>
                <td>{(row.certainty * 100).toFixed(0)}%</td>
                <td>${row.entry.toFixed(2)}</td>
                <td>${row.stop.toFixed(2)}</td>
                <td>${row.target.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
