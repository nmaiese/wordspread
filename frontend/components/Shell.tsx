import { Icon, Badge } from "@/components/ds";

/* TrustStrip + Footer + PageWrap — static editorial chrome around each screen. */

export function PageWrap({ children, narrow }: { children: React.ReactNode; narrow?: boolean }) {
  return (
    <div style={{ maxWidth: narrow ? "var(--content-narrow)" : "var(--content-max)", margin: "0 auto", padding: "0 var(--gutter)" }}>
      {children}
    </div>
  );
}

export function TrustStrip() {
  const items = [
    { icon: "shield-check", t: "Fonti ufficiali", d: "Solo resoconti e atti della Camera dei Deputati." },
    { icon: "quote", t: "Citazioni verificabili", d: "Ogni evidence rimanda al documento originale, con data e organo." },
    { icon: "check-circle", t: "Nessuna sintesi inventata", d: "Dove una fonte non è ancora parsabile, lo dichiariamo." },
  ];
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 14 }}>
      {items.map((it) => (
        <div key={it.t} style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
          <span style={{ color: "var(--teal-600)", display: "flex", marginTop: 2 }}>
            <Icon name={it.icon} size={20} />
          </span>
          <div>
            <div style={{ fontSize: 14.5, fontWeight: 600, color: "var(--ink-900)" }}>{it.t}</div>
            <div style={{ fontSize: 13, color: "var(--ink-500)", lineHeight: 1.5, marginTop: 2 }}>{it.d}</div>
          </div>
        </div>
      ))}
    </div>
  );
}

export function Footer() {
  return (
    <footer style={{ borderTop: "1px solid var(--border)", marginTop: 56, background: "var(--surface)" }}>
      <div
        style={{
          maxWidth: "var(--content-max)",
          margin: "0 auto",
          padding: "28px var(--gutter)",
          display: "flex",
          flexWrap: "wrap",
          gap: 16,
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div style={{ fontSize: 13, color: "var(--ink-500)", maxWidth: 560, lineHeight: 1.6 }}>
          <strong style={{ color: "var(--ink-700)" }}>Parla Mente</strong> — strumento di esplorazione pubblica dei dati parlamentari.
          Fonti: <span style={{ fontFamily: "var(--font-mono)", fontSize: 12 }}>dati.camera.it</span> · resoconti stenografici dell&apos;Assemblea.
        </div>
        <Badge tone="neutral" size="sm">
          Fase 1 · Camera dei Deputati
        </Badge>
      </div>
    </footer>
  );
}
