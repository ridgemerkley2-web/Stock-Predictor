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
        <h2 className="text-xl font-semibold">Risk Panel</h2>
        <p className="text-sm text-slate-400">
          Exposure, drawdown, and circuit breaker status.
        </p>
      </header>
      <div className="grid gap-4 md:grid-cols-2">
        {stats.map((stat) => (
          <div
            key={stat.label}
            className="rounded-xl border border-slate-800 bg-slate-900/40 p-5"
          >
            <div className="text-sm text-slate-400">{stat.label}</div>
            <div className="mt-2 text-2xl font-semibold">{stat.value}</div>
          </div>
        ))}
      </div>
    </main>
  );
}
