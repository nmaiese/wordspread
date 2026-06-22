import React from "react";
import { Icon } from "./Icon";

/* InterventionsTable — consultable list of official interventions. Readable rows,
   warm zebra, mono date/source. rows: { date, context, text, source_url }. */

export interface InterventionRow {
  id?: string;
  date?: string | null;
  context?: string;
  text?: string;
  source_url?: string;
}

export interface InterventionsTableProps extends React.HTMLAttributes<HTMLDivElement> {
  rows: InterventionRow[];
  maxChars?: number;
}

export function InterventionsTable({ rows = [], maxChars = 160, style = {}, ...rest }: InterventionsTableProps) {
  return (
    <div style={{ overflowX: "auto", ...style }} {...rest}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
        <thead>
          <tr>
            {["Data", "Sede", "Estratto", "Fonte"].map((h, i) => (
              <th
                key={h}
                style={{
                  textAlign: "left",
                  padding: "10px 12px",
                  fontFamily: "var(--font-mono)",
                  fontSize: 11,
                  fontWeight: 600,
                  letterSpacing: "0.06em",
                  textTransform: "uppercase",
                  color: "var(--text-muted)",
                  borderBottom: "1.5px solid var(--border-strong)",
                  whiteSpace: "nowrap",
                  width: i === 2 ? "auto" : 1,
                }}
              >
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={r.id || i} style={{ background: i % 2 ? "var(--surface-soft)" : "transparent" }}>
              <td
                style={{
                  padding: "11px 12px",
                  verticalAlign: "top",
                  fontFamily: "var(--font-mono)",
                  fontSize: 12.5,
                  color: "var(--text-muted)",
                  whiteSpace: "nowrap",
                  borderBottom: "1px solid var(--border-soft)",
                }}
              >
                {r.date || "—"}
              </td>
              <td
                style={{
                  padding: "11px 12px",
                  verticalAlign: "top",
                  color: "var(--text-body)",
                  whiteSpace: "nowrap",
                  borderBottom: "1px solid var(--border-soft)",
                }}
              >
                {r.context || "—"}
              </td>
              <td
                style={{
                  padding: "11px 12px",
                  verticalAlign: "top",
                  color: "var(--text-strong)",
                  lineHeight: 1.5,
                  borderBottom: "1px solid var(--border-soft)",
                }}
              >
                {r.text ? `${r.text.slice(0, maxChars)}${r.text.length > maxChars ? "…" : ""}` : "—"}
              </td>
              <td style={{ padding: "11px 12px", verticalAlign: "top", borderBottom: "1px solid var(--border-soft)" }}>
                <a
                  href={r.source_url || "#"}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: 4,
                    fontFamily: "var(--font-mono)",
                    fontSize: 12,
                    color: "var(--accent)",
                  }}
                >
                  link <Icon name="external-link" size={12} />
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
