import "./globals.css";
import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Parla Mente",
  description:
    "Capire di cosa parlano davvero deputati e senatori, partendo dalle fonti ufficiali.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="it">
      <body>
        <div className="container">
          <div className="brand">
            <h1>Parla Mente</h1>
            <span className="payoff">
              di cosa parlano davvero deputati e senatori, dalle fonti ufficiali
            </span>
          </div>
          <nav className="topnav">
            <Link href="/">Cerca</Link>
            <Link href="/compare">Confronta</Link>
          </nav>
          {children}
        </div>
      </body>
    </html>
  );
}
