import React from "react";
import { Icon } from "./Icon";
import { SourceLink } from "./SourceLink";
import { Badge } from "./Badge";

/* EvidenceCard — the inspectable proof unit. A verbatim quote from an official
   record + source metadata (document type, date, organ) + official link.
   Serif quote carries the editorial voice. */

export interface EvidenceCardProps extends React.HTMLAttributes<HTMLElement> {
  quote: string;
  topic?: string;
  documentType?: string;
  date?: string;
  organ?: string;
  url?: string;
}

export function EvidenceCard({
  quote,
  topic,
  documentType = "Resoconto stenografico",
  date,
  organ,
  url,
  style = {},
  ...rest
}: EvidenceCardProps) {
  return (
    <figure
      style={{
        margin: 0,
        background: "var(--surface-card)",
        border: "1px solid var(--border)",
        borderLeft: "3px solid var(--verify)",
        borderRadius: "var(--radius-md)",
        padding: "18px 20px",
        boxShadow: "var(--shadow-xs)",
        ...style,
      }}
      {...rest}
    >
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 10, marginBottom: 12 }}>
        {topic ? (
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: 11,
              letterSpacing: "0.06em",
              textTransform: "uppercase",
              color: "var(--text-muted)",
            }}
          >
            {topic}
          </span>
        ) : (
          <span />
        )}
        <Badge tone="verify" dot size="sm">
          Fonte ufficiale
        </Badge>
      </div>

      <blockquote
        style={{
          margin: 0,
          fontFamily: "var(--font-serif)",
          fontSize: "18px",
          lineHeight: 1.55,
          color: "var(--text-strong)",
          position: "relative",
        }}
      >
        <Icon
          name="quote"
          size={18}
          style={{ display: "inline", verticalAlign: "-2px", marginRight: 6, color: "var(--teal-500)", opacity: 0.85 }}
        />
        {quote}
      </blockquote>

      <figcaption
        style={{
          marginTop: 14,
          paddingTop: 12,
          borderTop: "1px solid var(--border-soft)",
          display: "flex",
          flexWrap: "wrap",
          alignItems: "center",
          gap: "10px 16px",
          fontFamily: "var(--font-mono)",
          fontSize: 12,
          color: "var(--text-muted)",
        }}
      >
        <span style={{ display: "inline-flex", alignItems: "center", gap: 5 }}>
          <Icon name="file-text" size={13} /> {documentType}
        </span>
        {organ && (
          <span style={{ display: "inline-flex", alignItems: "center", gap: 5 }}>
            <Icon name="building" size={13} /> {organ}
          </span>
        )}
        {date && (
          <span style={{ display: "inline-flex", alignItems: "center", gap: 5 }}>
            <Icon name="calendar" size={13} /> {date}
          </span>
        )}
        {url && (
          <span style={{ marginLeft: "auto" }}>
            <SourceLink href={url} size="sm" />
          </span>
        )}
      </figcaption>
    </figure>
  );
}
