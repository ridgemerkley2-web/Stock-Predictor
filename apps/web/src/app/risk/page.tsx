const stats = [
  { label: "Gross Exposure", value: "0.82x" },
  { label: "Daily PnL", value: "+$2,140" },
  { label: "Drawdown", value: "4.2%" },
  { label: "Circuit Breaker", value: "OK" },
];

export default function RiskPage() {
  return (
    <main className="space-y-4">
      <header>
        <h2 className="page-title">Risk Panel</h2>
        <p className="subtitle">
          Exposure, drawdown, and AI guardrails with neural regime filters.
        </p>
      </header>
      <div className="stat-grid">
        {stats.map((stat) => (
          <div key={stat.label} className="stat">
            <span>{stat.label}</span>
            <h3>{stat.value}</h3>
          </div>
        ))}
      </div>
    </main>
  );
}
