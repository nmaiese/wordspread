"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { searchPoliticians, PoliticianSummary } from "@/lib/api";

export function SearchBox({
  linkBase = "/politician",
}: {
  linkBase?: string;
}) {
  const [q, setQ] = useState("");
  const [chamber, setChamber] = useState("");
  const [results, setResults] = useState<PoliticianSummary[]>([]);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    const t = setTimeout(async () => {
      try {
        setErr(null);
        const r = await searchPoliticians({
          q: q || undefined,
          chamber: chamber || undefined,
          legislature: "19",
          limit: 30,
        });
        setResults(r);
      } catch (e: any) {
        setErr(e.message);
      }
    }, 250);
    return () => clearTimeout(t);
  }, [q, chamber]);

  return (
    <div>
      <div className="row">
        <input
          className="grow"
          placeholder="Cerca un parlamentare per nome…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <select value={chamber} onChange={(e) => setChamber(e.target.value)}>
          <option value="">Tutte le Camere</option>
          <option value="camera">Camera</option>
          <option value="senato">Senato</option>
        </select>
        <select disabled value="19">
          <option value="19">Legislatura 19</option>
        </select>
      </div>
      {err && <p className="note">Errore API: {err}. È avviato `parlamente api`?</p>}
      <ul className="list" style={{ marginTop: 14 }}>
        {results.map((p) => (
          <li key={p.id}>
            <Link href={`${linkBase}/${p.id}`}>
              <strong>{p.full_name}</strong>
            </Link>{" "}
            <span className="muted">
              · {p.chamber} · {p.group_name || "—"}
            </span>
          </li>
        ))}
        {results.length === 0 && !err && (
          <li className="muted">Nessun risultato.</li>
        )}
      </ul>
    </div>
  );
}
