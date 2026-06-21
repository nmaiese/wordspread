"use client";

import { useEffect, useState } from "react";
import { getProfile, Profile } from "@/lib/api";
import { TopicBar } from "@/components/TopicBar";
import { WordCloud } from "@/components/WordCloud";

export default function PoliticianPage({ params }: { params: { id: string } }) {
  const [p, setP] = useState<Profile | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    getProfile(params.id).then(setP).catch((e) => setErr(e.message));
  }, [params.id]);

  if (err) return <p className="note">Errore: {err}. È avviato `parlamente api`?</p>;
  if (!p) return <p className="muted">Caricamento…</p>;

  const period =
    p.kpi.period.from && p.kpi.period.to
      ? `${p.kpi.period.from} → ${p.kpi.period.to}`
      : "—";

  return (
    <div>
      <div className="panel">
        <h2 style={{ margin: "0 0 4px" }}>{p.politician.full_name}</h2>
        <div className="muted">
          {p.politician.chamber === "camera" ? "Camera dei Deputati" : p.politician.chamber} ·{" "}
          {p.politician.group_name || "—"} · Legislatura {p.politician.legislature}
          {p.politician.official_url && (
            <>
              {" "}·{" "}
              <a href={p.politician.official_url} target="_blank" rel="noreferrer">
                scheda ufficiale
              </a>
            </>
          )}
        </div>
        <div className="kpis" style={{ marginTop: 14 }}>
          <div className="kpi">
            <div className="n">{p.kpi.intervention_count}</div>
            <div className="l">interventi analizzati</div>
          </div>
          <div className="kpi">
            <div className="n">{p.kpi.act_count}</div>
            <div className="l">atti analizzati</div>
          </div>
          <div className="kpi">
            <div className="n">{p.kpi.topic_count}</div>
            <div className="l">temi rilevati</div>
          </div>
          <div className="kpi">
            <div className="n" style={{ fontSize: 14 }}>{period}</div>
            <div className="l">periodo coperto</div>
          </div>
        </div>
      </div>

      <div className="section-title">Top temi</div>
      <div className="panel">
        {p.top_topics.length === 0 && (
          <p className="muted">
            Nessun tema rilevato negli interventi disponibili (molti interventi
            possono essere procedurali).
          </p>
        )}
        {p.top_topics.map((t) => (
          <TopicBar
            key={t.topic_id}
            label={`${t.topic} · ${t.macro_area}`}
            share={t.share}
            sub={`${t.intervention_count} int / ${t.act_count} atti`}
          />
        ))}
      </div>

      <div className="section-title">Evidence — fonti verificabili</div>
      <div className="panel">
        {p.evidence.slice(0, 6).map((te) => (
          <div key={te.topic_id} style={{ marginBottom: 16 }}>
            <strong>{te.topic}</strong>{" "}
            <span className="muted">
              ({Math.round(te.score * 100)}% · {te.intervention_count} interventi)
            </span>
            <div>
              {te.keywords.map((k) => (
                <span key={k} className="badge">
                  {k}
                </span>
              ))}
            </div>
            {te.evidence.slice(0, 2).map((e, i) => (
              <div key={i}>
                <div className="quote">{e.quote}</div>
                <div className="src">
                  {e.document_type} · {e.date} ·{" "}
                  <a href={e.url} target="_blank" rel="noreferrer">
                    fonte ufficiale
                  </a>
                </div>
              </div>
            ))}
          </div>
        ))}
        {p.evidence.length === 0 && (
          <p className="muted">Nessuna evidence disponibile.</p>
        )}
      </div>

      <div className="section-title">Parole caratteristiche</div>
      <div className="panel">
        <WordCloud items={p.keywords} />
      </div>

      <div className="section-title">Interventi ufficiali</div>
      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Data</th>
              <th>Sede</th>
              <th>Estratto</th>
              <th>Fonte</th>
            </tr>
          </thead>
          <tbody>
            {p.interventions.slice(0, 30).map((it) => (
              <tr key={it.id}>
                <td>{it.date}</td>
                <td>{it.context}</td>
                <td>{it.text.slice(0, 180)}…</td>
                <td>
                  <a href={it.source_url} target="_blank" rel="noreferrer">
                    link
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {p.interventions.length === 0 && (
          <p className="muted">Nessun intervento disponibile.</p>
        )}
      </div>

      <div className="section-title">Atti ufficiali</div>
      <div className="panel">
        {p.acts.length === 0 ? (
          <p className="muted">
            Nessun atto caricato (l&apos;adapter atti è predisposto; vedi
            docs/sources-limits.md).
          </p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Data</th>
                <th>Tipo</th>
                <th>Titolo</th>
                <th>Fonte</th>
              </tr>
            </thead>
            <tbody>
              {p.acts.map((a) => (
                <tr key={a.id}>
                  <td>{a.date}</td>
                  <td>{a.act_type}</td>
                  <td>{a.title}</td>
                  <td>
                    <a href={a.source_url} target="_blank" rel="noreferrer">
                      link
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
