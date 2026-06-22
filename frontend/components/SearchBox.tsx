"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { searchPoliticians, PoliticianSummary } from "@/lib/api";
import { SearchBar, PoliticianResult, StateMessage } from "@/components/ds";
import { TrustStrip } from "@/components/Shell";

/* The home search experience: prominent search + filters, live results, trust strip.
   Filters chamber/legislature server-side; group is refined client-side. */

export function SearchBox({ linkBase = "/politician" }: { linkBase?: string }) {
  const router = useRouter();
  const [q, setQ] = useState("");
  const [chamber, setChamber] = useState("");
  const [legislature, setLegislature] = useState("19");
  const [group, setGroup] = useState("");
  const [results, setResults] = useState<PoliticianSummary[]>([]);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const t = setTimeout(async () => {
      try {
        setErr(null);
        setLoading(true);
        const r = await searchPoliticians({
          q: q || undefined,
          chamber: chamber || undefined,
          legislature: legislature || undefined,
          limit: 60,
        });
        setResults(r);
      } catch (e: any) {
        setErr(e.message);
      } finally {
        setLoading(false);
      }
    }, 250);
    return () => clearTimeout(t);
  }, [q, chamber, legislature]);

  const groups = useMemo(
    () => Array.from(new Set(results.map((p) => p.group_name).filter(Boolean))) as string[],
    [results]
  );

  const filtered = group ? results.filter((p) => p.group_name === group) : results;
  const active = Boolean(q || chamber || group);

  return (
    <div>
      <SearchBar
        value={q}
        onChange={setQ}
        chamber={chamber}
        onChamberChange={setChamber}
        legislature={legislature}
        onLegislatureChange={setLegislature}
        group={group}
        onGroupChange={setGroup}
        groups={groups}
      />

      <div style={{ padding: "32px 0 8px", display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 12 }}>
        <h2 style={{ fontSize: 19, fontWeight: 600, color: "var(--ink-900)" }}>
          {active ? "Risultati" : "Parlamentari analizzati"}
        </h2>
        <span style={{ fontFamily: "var(--font-mono)", fontSize: 13, color: "var(--ink-400)" }}>
          {filtered.length}
          {results.length !== filtered.length ? ` di ${results.length}` : ""}
        </span>
      </div>

      {err ? (
        <StateMessage
          kind="error"
          title="Impossibile contattare l'API"
          description={`${err}. Verifica che il backend sia avviato (parlamente api).`}
        />
      ) : loading && results.length === 0 ? (
        <StateMessage kind="loading" title="Caricamento…" />
      ) : filtered.length === 0 ? (
        <StateMessage kind="empty" title="Nessun risultato" description="Prova un altro nome o rimuovi un filtro." />
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 10, paddingBottom: 8 }}>
          {filtered.map((p) => (
            <PoliticianResult
              key={p.id}
              name={p.full_name}
              chamber={p.chamber}
              group={p.group_name}
              legislature={p.legislature}
              onClick={() => router.push(`${linkBase}/${p.id}`)}
            />
          ))}
        </div>
      )}

      <div style={{ marginTop: 40, padding: "28px 0 8px", borderTop: "1px solid var(--border-soft)" }}>
        <TrustStrip />
      </div>
    </div>
  );
}
