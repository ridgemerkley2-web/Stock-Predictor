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
    <main className="space-y-4">
      <header>
        <h2 className="text-xl font-semibold">Positions / Orders / Fills</h2>
        <p className="text-sm text-slate-400">
          Live portfolio view with Alpaca execution status.
        </p>
      </header>
      <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
        {positions.map((pos) => (
          <div key={pos.ticker} className="flex items-center justify-between py-2">
            <div>
              <div className="text-lg font-semibold">{pos.ticker}</div>
              <div className="text-sm text-slate-400">Qty {pos.qty}</div>
            </div>
            <div className="text-right">
              <div className="text-sm text-slate-300">Avg ${pos.avg.toFixed(2)}</div>
              <div className="text-sm text-emerald-400">
                +${pos.unrealized.toFixed(2)}
              </div>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
