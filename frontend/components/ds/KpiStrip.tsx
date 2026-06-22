import React from "react";

/* KpiStrip — overview figures at the top of a profile. One divided strip, not
   nested cards. Items: { value, label, hint?, small? }. */

export interface KpiItem {
  value: React.ReactNode;
  label: string;
  hint?: string;
  small?: boolean;
}

export interface KpiStripProps extends React.HTMLAttributes<HTMLDivElement> {
  items: KpiItem[];
}

export function KpiStrip({ items = [], style = {}, ...rest }: KpiStripProps) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: `repeat(${items.length || 1}, 1fr)`,
        background: "var(--surface-card)",
        border: "1px solid var(--border)",
        borderRadius: "var(--radius-lg)",
        overflow: "hidden",
        ...style,
      }}
      {...rest}
    >
      {items.map((it, i) => (
        <div key={i} style={{ padding: "18px 22px", borderLeft: i === 0 ? "none" : "1px solid var(--border-soft)", minWidth: 0 }}>
          <div
            style={{
              fontFamily: "var(--font-mono)",
              fontWeight: 600,
              fontSize: it.small ? "18px" : "30px",
              lineHeight: 1.05,
              color: "var(--text-strong)",
              fontFeatureSettings: '"tnum" 1',
              whiteSpace: "nowrap",
              overflow: "hidden",
              textOverflow: "ellipsis",
            }}
          >
            {it.value}
          </div>
          <div style={{ marginTop: 6, fontSize: "12.5px", color: "var(--text-muted)", fontWeight: 500, letterSpacing: "0.01em" }}>
            {it.label}
          </div>
          {it.hint && <div style={{ marginTop: 2, fontSize: "11px", color: "var(--text-faint)" }}>{it.hint}</div>}
        </div>
      ))}
    </div>
  );
}
