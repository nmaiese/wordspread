"use client";

import React from "react";
import { Avatar } from "./Avatar";
import { Badge } from "./Badge";
import { Icon } from "./Icon";

/* PoliticianResult — a search result / list row for one parliamentarian.
   Avatar + name + chamber/group + optional counts. Hover lifts. */

const CHAMBER_LABEL: Record<string, string> = { camera: "Camera", senato: "Senato" };

export interface PoliticianResultProps {
  name: string;
  chamber?: string;
  group?: string | null;
  legislature?: string;
  interventionCount?: number | null;
  topicCount?: number | null;
  tone?: "neutral" | "a" | "b" | "teal";
  onClick?: () => void;
  style?: React.CSSProperties;
}

export function PoliticianResult({
  name,
  chamber = "camera",
  group,
  legislature,
  interventionCount,
  topicCount,
  tone = "neutral",
  onClick,
  style = {},
}: PoliticianResultProps) {
  const [hover, setHover] = React.useState(false);
  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: "flex",
        alignItems: "center",
        gap: 16,
        padding: "14px 16px",
        textDecoration: "none",
        background: hover ? "var(--surface-hover)" : "var(--surface-card)",
        border: "1px solid var(--border)",
        borderRadius: "var(--radius-md)",
        cursor: "pointer",
        transition:
          "background var(--dur-fast) var(--ease-out), border-color var(--dur-fast) var(--ease-out), transform var(--dur-fast) var(--ease-out)",
        transform: hover ? "translateY(-1px)" : "none",
        borderColor: hover ? "var(--border-strong)" : "var(--border)",
        ...style,
      }}
    >
      <Avatar name={name} tone={tone} size={44} />
      <div style={{ minWidth: 0, flex: 1 }}>
        <div
          style={{
            fontSize: "16px",
            fontWeight: 600,
            color: "var(--text-strong)",
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
          }}
        >
          {name}
        </div>
        <div style={{ marginTop: 4, display: "flex", flexWrap: "wrap", alignItems: "center", gap: 8, fontSize: 13, color: "var(--text-muted)" }}>
          <Badge tone="neutral" size="sm">
            {CHAMBER_LABEL[chamber] || chamber}
          </Badge>
          <span style={{ whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", maxWidth: 280 }}>
            {group || "Gruppo non indicato"}
          </span>
          {legislature && <span style={{ fontFamily: "var(--font-mono)", fontSize: 12, color: "var(--text-faint)" }}>· Leg. {legislature}</span>}
        </div>
      </div>
      {(interventionCount != null || topicCount != null) && (
        <div style={{ display: "flex", gap: 20, flex: "none" }}>
          {interventionCount != null && (
            <div style={{ textAlign: "right" }}>
              <div style={{ fontFamily: "var(--font-mono)", fontWeight: 600, fontSize: 16, color: "var(--text-strong)", fontFeatureSettings: '"tnum" 1' }}>
                {interventionCount}
              </div>
              <div style={{ fontSize: 11, color: "var(--text-faint)" }}>interventi</div>
            </div>
          )}
          {topicCount != null && (
            <div style={{ textAlign: "right" }}>
              <div style={{ fontFamily: "var(--font-mono)", fontWeight: 600, fontSize: 16, color: "var(--text-strong)", fontFeatureSettings: '"tnum" 1' }}>
                {topicCount}
              </div>
              <div style={{ fontSize: 11, color: "var(--text-faint)" }}>temi</div>
            </div>
          )}
        </div>
      )}
      <Icon name="chevron-right" size={18} style={{ color: hover ? "var(--accent)" : "var(--text-faint)", flex: "none" }} />
    </div>
  );
}
