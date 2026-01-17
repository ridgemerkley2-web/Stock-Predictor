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
      <section className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">
        <h2 className="text-xl font-semibold">Mission Control</h2>
        <p className="mt-2 text-slate-300">
          Monitor candidate generation, risk state, and bundle promotion readiness in
          one place.
        </p>
        <div className="mt-4 flex gap-3">
          <button className="rounded-md bg-emerald-500 px-4 py-2 text-sm font-medium text-white">
            Enable Live Trading
          </button>
          <button className="rounded-md border border-slate-700 px-4 py-2 text-sm font-medium text-slate-200">
            Flatten All
          </button>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        {cards.map((card) => (
          <div
            key={card.title}
            className="rounded-xl border border-slate-800 bg-slate-900/40 p-5"
          >
            <h3 className="text-lg font-semibold">{card.title}</h3>
            <p className="mt-2 text-sm text-slate-400">{card.description}</p>
          </div>
        ))}
      </section>
    </main>
  );
}
