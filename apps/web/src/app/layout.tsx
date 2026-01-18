import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Stock Predictor",
  description: "Alpaca algo trading control center",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="page">
          <header className="top-bar">
            <div className="brand">
              <h1>Stock Predictor</h1>
              <p>Production-style Alpaca trading console</p>
            </div>
            <nav className="nav-links">
              <a href="/">Overview</a>
              <a href="/best-buys">Best Buys Now</a>
              <a href="/positions">Positions</a>
              <a href="/risk">Risk</a>
              <a href="/research">Research</a>
            </nav>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
