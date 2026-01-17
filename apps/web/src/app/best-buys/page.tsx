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
        <h2 className="text-xl font-semibold">Best Buys Now</h2>
        <p className="text-sm text-slate-400">
          Live ranked candidates with certainty and expected value.
        </p>
      </header>
      <div className="overflow-hidden rounded-xl border border-slate-800">
        <table className="w-full text-sm">
          <thead className="bg-slate-900/80 text-left text-slate-300">
            <tr>
              <th className="px-4 py-3">Ticker</th>
              <th className="px-4 py-3">EV</th>
              <th className="px-4 py-3">Certainty</th>
              <th className="px-4 py-3">Entry</th>
              <th className="px-4 py-3">Stop</th>
              <th className="px-4 py-3">Target</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.ticker} className="border-t border-slate-800">
                <td className="px-4 py-3 font-medium">{row.ticker}</td>
                <td className="px-4 py-3">{row.ev.toFixed(2)}</td>
                <td className="px-4 py-3">{(row.certainty * 100).toFixed(0)}%</td>
                <td className="px-4 py-3">${row.entry.toFixed(2)}</td>
                <td className="px-4 py-3">${row.stop.toFixed(2)}</td>
                <td className="px-4 py-3">${row.target.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
