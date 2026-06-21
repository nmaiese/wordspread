"use client";

import { useEffect, useState } from "react";
import { searchPoliticians, compare, PoliticianSummary } from "@/lib/api";
import { TopicBar } from "@/components/TopicBar";

function Picker({
  label,
  value,
  onChange,
}: {
  label: string;
  value: string;
  onChange: (id: string) => void;
}) {
  const [q, setQ] = useState("");
  const [opts, setOpts] = useState<PoliticianSummary[]>([]);
  useEffect(() => {
    const t = setTimeout(() => {
      searchPoliticians({ q: q || undefined, legislature: "19", limit: 20 })
        .then(setOpts)
        .catch(() => setOpts([]));
    }, 250);
    return () => clearTimeout(t);
  }, [q]);
  return (
    <div className="grow">
      <div className="muted" style={{ marginBottom: 6 }}>{label}</div>
      <input
        placeholder="filtra per nome…"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        style={{ width: "100%", marginBottom: 8 }}
      />
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        style={{ width: "100%" }}
        size={6}
      >
        {opts.map((o) => (
          <option key={o.id} value={o.id}>
            {o.full_name} — {o.group_name || "—"}
          </option>
        ))}
      </select>
    </div>
  );
}

export default function ComparePage() {
  const [a, setA] = useState("");
  const [b, setB] = useState("");
  const [data, setData] = useState<any>(null);
  const [err, setErr] = useState<string | null>(null);

  async function run() {
    if (!a || !b) return;
    try {
      setErr(null);
      setData(await compare(a, b));
    } catch (e: any) {
      setErr(e.message);
    }
  }

  return (
    <div>
      <div className="panel">
        <div className="row">
          <Picker label="Parlamentare A" value={a} onChange={setA} />
          <Picker label="Parlamentare B" value={b} onChange={setB} />
        </div>
        <button className="primary" style={{ marginTop: 14 }} onClick={run} disabled={!a || !b}>
          Confronta
        </button>
        {err && <p className="note">Errore: {err}</p>}
      </div>

      {data && (
        <>
          <div className="section-title">
            {data.a.full_name} vs {data.b.full_name}
          </div>
          <div className="row">
            <div className="panel grow">
              <strong>Volumi per sede</strong>
              <p className="muted" style={{ fontSize: 13 }}>
                {data.a.full_name}: aula {data.venues.a.aula || 0} · commissione{" "}
                {data.venues.a.commissione || 0} · atti {data.venues.a.atti || 0}
                <br />
                {data.b.full_name}: aula {data.venues.b.aula || 0} · commissione{" "}
                {data.venues.b.commissione || 0} · atti {data.venues.b.atti || 0}
              </p>
            </div>
          </div>

          <div className="section-title">Temi comuni</div>
          <div className="panel">
            {data.common_topics.length === 0 && (
              <p className="muted">Nessun tema in comune nei dati disponibili.</p>
            )}
            {data.common_topics.map((c: any) => (
              <div key={c.topic_id} style={{ marginBottom: 10 }}>
                <div className="muted" style={{ fontSize: 13 }}>{c.topic}</div>
                <TopicBar label={data.a.full_name} share={c.share_a} />
                <TopicBar label={data.b.full_name} share={c.share_b} />
              </div>
            ))}
          </div>

          <div className="row">
            <div className="panel grow">
              <strong>Temi distintivi — {data.a.full_name}</strong>
              <div style={{ marginTop: 8 }}>
                {data.distinctive_a.map((t: any) => (
                  <span key={t.topic_id} className="badge">{t.topic}</span>
                ))}
                {data.distinctive_a.length === 0 && <span className="muted">—</span>}
              </div>
              <div className="note">Keyword: {data.distinctive_keywords_a.join(", ") || "—"}</div>
            </div>
            <div className="panel grow">
              <strong>Temi distintivi — {data.b.full_name}</strong>
              <div style={{ marginTop: 8 }}>
                {data.distinctive_b.map((t: any) => (
                  <span key={t.topic_id} className="badge">{t.topic}</span>
                ))}
                {data.distinctive_b.length === 0 && <span className="muted">—</span>}
              </div>
              <div className="note">Keyword: {data.distinctive_keywords_b.join(", ") || "—"}</div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
