"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { searchPoliticians, compare, PoliticianSummary } from "@/lib/api";
import { PageWrap } from "@/components/Shell";
import { Avatar, Select, Button, Tag, ComparisonRow, StateMessage } from "@/components/ds";

function PickerColumn({
  label,
  side,
  value,
  onChange,
  options,
}: {
  label: string;
  side: "a" | "b";
  value: string;
  onChange: (id: string) => void;
  options: PoliticianSummary[];
}) {
  const sel = options.find((o) => o.id === value);
  const accent = side === "a" ? "var(--coral-600)" : "var(--violet-600)";
  return (
    <div
      style={{
        background: "var(--surface)",
        border: "1px solid var(--border)",
        borderTop: `3px solid ${accent}`,
        borderRadius: "var(--radius-lg)",
        padding: 18,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 12 }}>
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: 11,
            letterSpacing: "0.08em",
            textTransform: "uppercase",
            color: accent,
            fontWeight: 600,
          }}
        >
          Parlamentare {label}
        </span>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
        <Avatar name={sel ? sel.full_name : "?"} tone={side} size={40} />
        <div style={{ minWidth: 0 }}>
          <div style={{ fontSize: 16, fontWeight: 600, color: "var(--ink-900)", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
            {sel ? sel.full_name : "Seleziona"}
          </div>
          <div style={{ fontSize: 13, color: "var(--ink-500)" }}>{sel ? sel.group_name || "—" : "—"}</div>
        </div>
      </div>
      <Select value={value} onChange={(e) => onChange(e.target.value)} containerStyle={{ width: "100%" }} style={{ width: "100%" }}>
        <option value="">Seleziona un parlamentare…</option>
        {options.map((o) => (
          <option key={o.id} value={o.id}>
            {o.full_name} — {o.group_name || "—"}
          </option>
        ))}
      </Select>
    </div>
  );
}

function CompareInner() {
  const params = useSearchParams();
  const [opts, setOpts] = useState<PoliticianSummary[]>([]);
  const [a, setA] = useState(params.get("a") || "");
  const [b, setB] = useState(params.get("b") || "");
  const [data, setData] = useState<any>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    searchPoliticians({ legislature: "19", limit: 200 })
      .then(setOpts)
      .catch(() => setOpts([]));
  }, []);

  useEffect(() => {
    if (!a || !b) {
      setData(null);
      return;
    }
    let cancelled = false;
    setErr(null);
    compare(a, b)
      .then((d) => !cancelled && setData(d))
      .catch((e) => !cancelled && setErr(e.message));
    return () => {
      cancelled = true;
    };
  }, [a, b]);

  return (
    <main>
      <PageWrap>
        <div style={{ padding: "32px 0 8px", maxWidth: 720 }}>
          <div className="pm-eyebrow" style={{ marginBottom: 8 }}>Confronto</div>
          <h1 style={{ fontFamily: "var(--font-serif)", fontWeight: 600, fontSize: 36, letterSpacing: "-0.02em", color: "var(--ink-900)", margin: 0 }}>
            A · vs · B
          </h1>
          <p style={{ fontSize: 16, color: "var(--ink-500)", marginTop: 12, lineHeight: 1.55 }}>
            Confronta due parlamentari per temi comuni e distintivi. Le differenze sono mostrate su scala di quota:{" "}
            <span style={{ color: "var(--coral-700)", fontWeight: 600 }}>A in corallo</span>,{" "}
            <span style={{ color: "var(--violet-700)", fontWeight: 600 }}>B in viola</span>.
          </p>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginTop: 8 }}>
          <PickerColumn label="A" side="a" value={a} onChange={setA} options={opts} />
          <PickerColumn label="B" side="b" value={b} onChange={setB} options={opts} />
        </div>

        {err && (
          <div style={{ marginTop: 24 }}>
            <StateMessage kind="error" title="Confronto non disponibile" description={err} />
          </div>
        )}

        {!err && (!a || !b) && (
          <div style={{ marginTop: 24 }}>
            <StateMessage kind="empty" title="Seleziona due parlamentari" description="Scegli A e B per vedere temi comuni e distintivi." />
          </div>
        )}

        {!err && data && (
          <>
            {/* Venues */}
            <div style={{ marginTop: 24, display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: 12 }}>
              {[
                { k: "Interventi in Aula", a: data.venues?.a?.aula || 0, b: data.venues?.b?.aula || 0 },
                { k: "Commissione", a: data.venues?.a?.commissione || 0, b: data.venues?.b?.commissione || 0 },
                { k: "Atti", a: data.venues?.a?.atti || 0, b: data.venues?.b?.atti || 0 },
              ].map((v) => (
                <div key={v.k} style={{ background: "var(--surface)", border: "1px solid var(--border)", borderRadius: "var(--radius-md)", padding: "14px 16px" }}>
                  <div style={{ fontSize: 12, color: "var(--ink-500)", marginBottom: 8 }}>{v.k}</div>
                  <div style={{ display: "flex", gap: 16, fontFamily: "var(--font-mono)", fontWeight: 600, fontSize: 20 }}>
                    <span style={{ color: "var(--coral-700)" }}>{v.a}</span>
                    <span style={{ color: "var(--ink-300)" }}>/</span>
                    <span style={{ color: "var(--violet-700)" }}>{v.b}</span>
                  </div>
                </div>
              ))}
            </div>

            {/* Common topics */}
            <h2 style={{ fontFamily: "var(--font-serif)", fontWeight: 600, fontSize: 24, margin: "36px 0 6px", letterSpacing: "-0.015em" }}>
              Temi comuni
            </h2>
            <div style={{ background: "var(--surface)", border: "1px solid var(--border)", borderRadius: "var(--radius-lg)", padding: "10px 22px" }}>
              {data.common_topics?.length ? (
                data.common_topics.map((c: any) => <ComparisonRow key={c.topic_id} topic={c.topic} shareA={c.share_a} shareB={c.share_b} />)
              ) : (
                <div style={{ padding: "16px 0", color: "var(--ink-500)", fontSize: 14, textAlign: "center" }}>
                  Nessun tema in comune nei dati disponibili.
                </div>
              )}
            </div>

            {/* Distinctive */}
            <h2 style={{ fontFamily: "var(--font-serif)", fontWeight: 600, fontSize: 24, margin: "36px 0 6px", letterSpacing: "-0.015em" }}>
              Temi distintivi
            </h2>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, paddingBottom: 8 }}>
              {[
                {
                  side: "a" as const,
                  name: data.a?.full_name,
                  list: data.distinctive_a || [],
                  kws: data.distinctive_keywords_a || [],
                  accent: "var(--coral-600)",
                },
                {
                  side: "b" as const,
                  name: data.b?.full_name,
                  list: data.distinctive_b || [],
                  kws: data.distinctive_keywords_b || [],
                  accent: "var(--violet-600)",
                },
              ].map((col) => (
                <div
                  key={col.side}
                  style={{
                    background: "var(--surface)",
                    border: "1px solid var(--border)",
                    borderLeft: `3px solid ${col.accent}`,
                    borderRadius: "var(--radius-md)",
                    padding: 18,
                  }}
                >
                  <div style={{ fontSize: 15, fontWeight: 600, color: "var(--ink-900)", marginBottom: 10 }}>{col.name}</div>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 12 }}>
                    {col.list.length ? (
                      col.list.map((t: any) => (
                        <Tag key={t.topic_id} tone={col.side}>
                          {t.topic}
                        </Tag>
                      ))
                    ) : (
                      <span style={{ color: "var(--ink-400)", fontSize: 13 }}>—</span>
                    )}
                  </div>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 12, color: "var(--ink-400)" }}>
                    Keyword: {col.kws.length ? col.kws.join(" · ") : "—"}
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        <div style={{ height: 24 }} />
      </PageWrap>
    </main>
  );
}

export default function ComparePage() {
  return (
    <Suspense fallback={<PageWrap><div style={{ padding: "60px 0" }}><StateMessage kind="loading" title="Caricamento…" /></div></PageWrap>}>
      <CompareInner />
    </Suspense>
  );
}
