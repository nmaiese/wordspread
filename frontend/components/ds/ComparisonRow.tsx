import React from "react";

/* ComparisonRow — one topic with two opposed shares: side A (coral, grows toward
   centre from the right) and side B (violet, grows right). Immediate visual
   difference, no legend beyond the colours. */

export interface ComparisonRowProps extends React.HTMLAttributes<HTMLDivElement> {
  topic: string;
  shareA?: number;
  shareB?: number;
}

export function ComparisonRow({ topic, shareA = 0, shareB = 0, style = {}, ...rest }: ComparisonRowProps) {
  const pa = Math.round(shareA * 100);
  const pb = Math.round(shareB * 100);
  return (
    <div style={{ padding: "10px 0", ...style }} {...rest}>
      <div style={{ textAlign: "center", fontSize: "13.5px", fontWeight: 500, color: "var(--text-strong)", marginBottom: 8 }}>
        {topic}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 56px 1fr", alignItems: "center", gap: 10 }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "flex-end", gap: 8 }}>
          <span style={{ fontFamily: "var(--font-mono)", fontSize: 12, color: "var(--coral-700)", fontFeatureSettings: '"tnum" 1' }}>
            {pa}%
          </span>
          <div
            style={{
              flex: 1,
              background: "var(--paper-sunk)",
              borderRadius: "var(--radius-pill)",
              height: 10,
              overflow: "hidden",
              display: "flex",
              justifyContent: "flex-end",
            }}
          >
            <div
              style={{
                width: `${Math.max(1, pa)}%`,
                height: "100%",
                background: "var(--coral-600)",
                borderRadius: "var(--radius-pill)",
                transition: "width var(--dur-slow) var(--ease-out)",
              }}
            />
          </div>
        </div>
        <div style={{ textAlign: "center", fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-faint)", letterSpacing: "0.08em" }}>
          A · B
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <div style={{ flex: 1, background: "var(--paper-sunk)", borderRadius: "var(--radius-pill)", height: 10, overflow: "hidden" }}>
            <div
              style={{
                width: `${Math.max(1, pb)}%`,
                height: "100%",
                background: "var(--violet-600)",
                borderRadius: "var(--radius-pill)",
                transition: "width var(--dur-slow) var(--ease-out)",
              }}
            />
          </div>
          <span style={{ fontFamily: "var(--font-mono)", fontSize: 12, color: "var(--violet-700)", fontFeatureSettings: '"tnum" 1' }}>
            {pb}%
          </span>
        </div>
      </div>
    </div>
  );
}
