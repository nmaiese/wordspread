import { SearchBox } from "@/components/SearchBox";
import { PageWrap } from "@/components/Shell";

export default function HomePage() {
  return (
    <main>
      {/* Hero — editorial, but search is the payload */}
      <div style={{ borderBottom: "1px solid var(--border)", background: "var(--surface)" }}>
        <PageWrap>
          <div style={{ padding: "52px 0 40px", maxWidth: 820 }}>
            <div className="pm-eyebrow" style={{ marginBottom: 14 }}>
              Camera dei Deputati · Legislatura 19
            </div>
            <h1
              style={{
                fontFamily: "var(--font-serif)",
                fontWeight: 600,
                fontSize: "clamp(38px, 6vw, 60px)",
                lineHeight: 1.04,
                letterSpacing: "-0.025em",
                color: "var(--ink-900)",
                margin: 0,
              }}
            >
              Capire di cosa parlano
              <br />
              davvero i parlamentari.
            </h1>
            <p style={{ fontSize: 19, lineHeight: 1.55, color: "var(--ink-500)", marginTop: 18, marginBottom: 30, maxWidth: 620 }}>
              Profili, temi ricorrenti e citazioni dei deputati italiani, ricostruiti a partire dalle{" "}
              <strong style={{ color: "var(--ink-700)" }}>fonti parlamentari ufficiali</strong>. Ogni dato è tracciabile.
            </p>
          </div>
        </PageWrap>
      </div>

      <PageWrap>
        <div style={{ paddingTop: 28 }}>
          <SearchBox />
        </div>
      </PageWrap>
    </main>
  );
}
