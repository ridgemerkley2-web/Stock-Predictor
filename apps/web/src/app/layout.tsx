import type { ReactNode } from "react";

export const metadata = {
  title: "Stock Predictor",
  description: "Alpaca algo trading control center",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-950 text-slate-100">
        <div className="mx-auto max-w-6xl px-6 py-8">
          <header className="mb-8 flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-semibold">Stock Predictor</h1>
              <p className="text-sm text-slate-400">
                Production-style Alpaca trading console
              </p>
            </div>
            <nav className="flex gap-4 text-sm text-slate-300">
              <a href="/" className="hover:text-white">
                Overview
              </a>
              <a href="/best-buys" className="hover:text-white">
                Best Buys Now
              </a>
              <a href="/positions" className="hover:text-white">
                Positions
              </a>
              <a href="/risk" className="hover:text-white">
                Risk
              </a>
              <a href="/research" className="hover:text-white">
                Research
              </a>
            </nav>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
