"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getProfile, Profile } from "@/lib/api";
import { PageWrap } from "@/components/Shell";
import {
  Avatar,
  Badge,
  Button,
  Icon,
  KpiStrip,
  TopicBar,
  EvidenceCard,
  WordCloudPanel,
  InterventionsTable,
  SourceLink,
  DataLimitNote,
  StateMessage,
} from "@/components/ds";

function SectionHead({ eyebrow, title, hint }: { eyebrow?: string; title: string; hint?: string }) {
  return (
    <div style={{ margin: "36px 0 14px" }}>
      {eyebrow && <div className="pm-eyebrow" style={{ marginBottom: 6 }}>{eyebrow}</div>}
      <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 12, flexWrap: "wrap" }}>
        <h2 style={{ fontFamily: "var(--font-serif)", fontWeight: 600, fontSize: 26, letterSpacing: "-0.015em", color: "var(--ink-900)" }}>
          {title}
        </h2>
        {hint && <span style={{ fontSize: 13, color: "var(--ink-400)" }}>{hint}</span>}
      </div>
    </div>
  );
}

function Panel({ children, pad = 22 }: { children: React.ReactNode; pad?: number | string }) {
  return (
    <div style={{ background: "var(--surface)", border: "1px solid var(--border)", borderRadius: "var(--radius-lg)", padding: pad }}>
      {children}
    </div>
  );
}

export default function PoliticianPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [p, setP] = useState<Profile | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    getProfile(params.id)
      .then(setP)
      .catch((e) => setErr(e.message));
  }, [params.id]);

  if (err)
    return (
      <PageWrap>
        <div style={{ padding: "60px 0" }}>
          <StateMessage
            kind="error"
            title="Profilo non disponibile"
            description={`${err}. Verifica che il backend sia avviato (parlamente api).`}
          />
        </div>
      </PageWrap>
    );

  if (!p)
    return (
      <PageWrap>
        <div style={{ padding: "60px 0" }}>
          <StateMessage kind="loading" title="Caricamento profilo…" />
        </div>
      </PageWrap>
    );

  const period = p.kpi.period.from && p.kpi.period.to ? `${p.kpi.period.from} → ${p.kpi.period.to}` : "—";

  return (
    <main>
      {/* Header band */}
      <div style={{ borderBottom: "1px solid var(--border)", background: "var(--surface)" }}>
        <PageWrap>
          <div style={{ padding: "20px 0 26px" }}>
            <button
              onClick={() => router.push("/")}
              style={{
                background: "none",
                border: "none",
                cursor: "pointer",
                color: "var(--ink-500)",
                fontSize: 13,
                display: "inline-flex",
                alignItems: "center",
                gap: 5,
                padding: 0,
                marginBottom: 18,
                fontFamily: "var(--font-ui)",
              }}
            >
              <Icon name="chevron-right" size={14} style={{ transform: "rotate(180deg)" }} /> Tutti i parlamentari
            </button>
            <div style={{ display: "flex", gap: 18, alignItems: "flex-start", flexWrap: "wrap" }}>
              <Avatar name={p.politician.full_name} size={64} tone="teal" />
              <div style={{ flex: 1, minWidth: 240 }}>
                <h1 style={{ fontFamily: "var(--font-serif)", fontWeight: 600, fontSize: 34, letterSpacing: "-0.02em", color: "var(--ink-900)", margin: 0 }}>
                  {p.politician.full_name}
                </h1>
                <div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: 10, marginTop: 10 }}>
                  <Badge tone="neutral">{p.politician.chamber === "camera" ? "Camera dei Deputati" : p.politician.chamber}</Badge>
                  <span style={{ fontSize: 14.5, color: "var(--ink-700)", fontWeight: 500 }}>{p.politician.group_name || "Gruppo non indicato"}</span>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 12.5, color: "var(--ink-400)" }}>Leg. {p.politician.legislature}</span>
                </div>
              </div>
              <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
                {p.politician.official_url && (
                  <Button variant="secondary" iconRight="external-link" onClick={() => window.open(p.politician.official_url!, "_blank")}>
                    Scheda ufficiale
                  </Button>
                )}
                <Button variant="ghost" iconLeft="git-compare" onClick={() => router.push(`/compare?a=${encodeURIComponent(p.politician.id)}`)}>
                  Confronta
                </Button>
              </div>
            </div>
          </div>
        </PageWrap>
      </div>

      <PageWrap>
        {/* KPI overview */}
        <div style={{ marginTop: 26 }}>
          <KpiStrip
            items={[
              { value: p.kpi.intervention_count, label: "interventi analizzati" },
              { value: p.kpi.topic_count, label: "temi rilevati" },
              { value: period, label: "periodo coperto", small: true },
              { value: p.kpi.act_count, label: "atti", hint: p.kpi.act_count === 0 ? "non ancora popolati" : undefined },
            ]}
          />
        </div>

        {/* Two-column: topics + word cloud */}
        <div style={{ display: "grid", gridTemplateColumns: "minmax(0, 1.5fr) minmax(0, 1fr)", gap: 24, alignItems: "start" }}>
          <div>
            <SectionHead title="Top temi rilevati" hint="quota sugli interventi" />
            <Panel pad="8px 20px">
              {p.top_topics.length === 0 ? (
                <div style={{ padding: "16px 0", color: "var(--ink-500)", fontSize: 14 }}>
                  Nessun tema rilevato negli interventi disponibili (molti interventi possono essere procedurali).
                </div>
              ) : (
                p.top_topics.map((t) => (
                  <TopicBar
                    key={t.topic_id}
                    label={t.topic}
                    macroArea={t.macro_area}
                    share={t.share}
                    sub={`${t.intervention_count} int / ${t.act_count} atti`}
                  />
                ))
              )}
            </Panel>
          </div>
          <div>
            <SectionHead title="Parole caratteristiche" />
            <Panel>
              <WordCloudPanel items={p.keywords} />
              <div
                style={{
                  marginTop: 14,
                  paddingTop: 12,
                  borderTop: "1px solid var(--border-soft)",
                  fontSize: 12,
                  color: "var(--ink-400)",
                  display: "flex",
                  alignItems: "center",
                  gap: 6,
                }}
              >
                <Icon name="info" size={13} /> Dimensione proporzionale alla rilevanza (TF-IDF).
              </div>
            </Panel>
          </div>
        </div>

        {/* Evidence */}
        <SectionHead eyebrow="Citazioni verificabili" title="Evidence" hint="estratte dai resoconti ufficiali" />
        {p.evidence.length === 0 ? (
          <DataLimitNote title="Nessuna evidence">
            Nessuna citazione verificabile è ancora disponibile per questo profilo.
          </DataLimitNote>
        ) : (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(380px, 1fr))", gap: 16 }}>
            {p.evidence
              .filter((te) => te.evidence.length > 0)
              .slice(0, 6)
              .map((te) => {
                const ev = te.evidence[0];
                return (
                  <EvidenceCard
                    key={te.topic_id}
                    topic={te.topic}
                    quote={ev.quote}
                    documentType={ev.document_type}
                    organ={ev.source}
                    date={ev.date}
                    url={ev.url}
                  />
                );
              })}
          </div>
        )}

        {/* Interventions table */}
        <SectionHead title="Interventi ufficiali" hint={`${p.interventions.length} disponibili`} />
        {p.interventions.length === 0 ? (
          <DataLimitNote title="Nessun intervento">Nessun intervento disponibile per questo profilo.</DataLimitNote>
        ) : (
          <Panel pad="6px 8px">
            <InterventionsTable rows={p.interventions.slice(0, 30)} />
          </Panel>
        )}

        {/* Acts — dataset limit */}
        <SectionHead title="Atti" />
        {p.acts.length === 0 ? (
          <DataLimitNote>
            Gli <strong>atti</strong> (interrogazioni, mozioni, proposte di legge) non sono ancora popolati per questo profilo:
            l&apos;adapter è predisposto, ma l&apos;attribuzione atto→primo firmatario non è stata ancora risolta in modo affidabile.
            Vedi{" "}
            <SourceLink href="https://github.com/nmaiese/wordspread/blob/parla-mente/docs/sources-limits.md">docs/sources-limits</SourceLink>.
          </DataLimitNote>
        ) : (
          <Panel pad="6px 8px">
            <InterventionsTable
              rows={p.acts.map((a) => ({ id: a.id, date: a.date, context: a.act_type, text: a.title, source_url: a.source_url }))}
            />
          </Panel>
        )}

        <div style={{ height: 24 }} />
      </PageWrap>
    </main>
  );
}
