const positions = [
  {
    ticker: "AAPL",
    qty: 120,
    avg: 195.2,
    unrealized: 340.5,
  },
];

export default function PositionsPage() {
  return (
    <main className="page-stack">
      <header>
        <h2 className="page-title">Positions / Orders / Fills</h2>
        <p className="subtitle">
          Live portfolio view with AI conviction layers and neural signal overlays.
        </p>
      </header>
      <div className="card">
        {positions.map((pos) => (
          <div key={pos.ticker} className="list-item">
            <div>
              <div className="page-title">{pos.ticker}</div>
              <div className="subtitle">Qty {pos.qty}</div>
            </div>
            <div>
              <div className="subtitle">Avg ${pos.avg.toFixed(2)}</div>
              <div className="highlight">+${pos.unrealized.toFixed(2)}</div>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
