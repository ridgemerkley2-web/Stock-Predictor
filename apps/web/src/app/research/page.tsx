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
        <h2 className="text-xl font-semibold">Research Dashboard</h2>
        <p className="text-sm text-slate-400">
          Latest bundles and holdout results with promotion gates.
        </p>
      </header>
      <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
        {bundles.map((bundle) => (
          <div key={bundle.id} className="flex items-center justify-between py-2">
            <div>
              <div className="text-lg font-semibold">{bundle.id}</div>
              <div className="text-sm text-slate-400">Status: {bundle.status}</div>
            </div>
            <div className="text-right text-sm text-slate-300">
              <div>Sharpe {bundle.sharpe}</div>
              <div>Holdout {bundle.holdout}</div>
            </div>
          </div>
        ))}
        <div className="mt-4 flex gap-3">
          <button className="rounded-md bg-indigo-500 px-4 py-2 text-sm font-medium text-white">
            Select Bundle
          </button>
          <button className="rounded-md border border-slate-700 px-4 py-2 text-sm font-medium text-slate-200">
            Promote Bundle
          </button>
        </div>
      </div>
    </main>
  );
}
