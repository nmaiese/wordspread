import React from "react";

/* TopicBar — a readable horizontal share bar for one topic. */

type Tone = "teal" | "a" | "b" | "neutral";

const FILLS: Record<Tone, string> = {
  teal: "var(--teal-500)",
  a: "var(--coral-600)",
  b: "var(--violet-600)",
  neutral: "var(--ink-700)",
};

export interface TopicBarProps extends React.HTMLAttributes<HTMLDivElement> {
  label: React.ReactNode;
  macroArea?: string;
  share?: number;
  sub?: string;
  tone?: Tone;
}

export function TopicBar({ label, macroArea, share = 0, sub, tone = "teal", style = {}, ...rest }: TopicBarProps) {
  const pct = Math.round(share * 100);
  return (
    <div style={{ padding: "9px 0", ...style }} {...rest}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", gap: 12, marginBottom: 7 }}>
        <span style={{ fontSize: "14.5px", fontWeight: 500, color: "var(--text-strong)" }}>
          {label}
          {macroArea && <span style={{ color: "var(--text-faint)", fontWeight: 400 }}> · {macroArea}</span>}
        </span>
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "13px",
            color: "var(--text-muted)",
            flex: "none",
            fontFeatureSettings: '"tnum" 1',
          }}
        >
          {pct}%{sub ? ` · ${sub}` : ""}
        </span>
      </div>
      <div style={{ background: "var(--paper-sunk)", borderRadius: "var(--radius-pill)", height: 8, overflow: "hidden" }}>
        <div
          style={{
            width: `${Math.max(2, pct)}%`,
            height: "100%",
            background: FILLS[tone] || FILLS.teal,
            borderRadius: "var(--radius-pill)",
            transition: "width var(--dur-slow) var(--ease-out)",
          }}
        />
      </div>
    </div>
  );
}
