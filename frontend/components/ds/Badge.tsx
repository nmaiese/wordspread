import React from "react";

/* Badge — small status pill. Signature is the petrol "Fonte ufficiale" badge. */

type Tone = "verify" | "pending" | "neutral" | "a" | "b" | "danger" | "info";

const TONES: Record<Tone, { bg: string; fg: string; bd: string; dot: string }> = {
  verify: { bg: "var(--teal-50)", fg: "var(--teal-700)", bd: "var(--teal-100)", dot: "var(--teal-600)" },
  pending: { bg: "var(--ochre-50)", fg: "var(--ochre-700)", bd: "var(--ochre-100)", dot: "var(--ochre-600)" },
  neutral: { bg: "var(--paper-sunk)", fg: "var(--ink-500)", bd: "var(--line)", dot: "var(--ink-400)" },
  a: { bg: "var(--coral-50)", fg: "var(--coral-700)", bd: "var(--coral-100)", dot: "var(--coral-600)" },
  b: { bg: "var(--violet-50)", fg: "var(--violet-700)", bd: "var(--violet-100)", dot: "var(--violet-600)" },
  danger: { bg: "var(--error-100)", fg: "var(--error-600)", bd: "var(--error-100)", dot: "var(--error-600)" },
  info: { bg: "var(--surface-card)", fg: "var(--ink-700)", bd: "var(--border-strong)", dot: "var(--ink-500)" },
};

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  tone?: Tone;
  dot?: boolean;
  size?: "sm" | "md";
}

export function Badge({ children, tone = "neutral", dot = false, size = "md", style = {}, ...rest }: BadgeProps) {
  const t = TONES[tone] || TONES.neutral;
  const pad = size === "sm" ? "2px 8px" : "3px 10px";
  const fs = size === "sm" ? "11px" : "12px";
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "6px",
        padding: pad,
        fontSize: fs,
        fontFamily: "var(--font-mono)",
        fontWeight: 500,
        letterSpacing: "0.02em",
        color: t.fg,
        background: t.bg,
        border: `1px solid ${t.bd}`,
        borderRadius: "var(--radius-pill)",
        whiteSpace: "nowrap",
        lineHeight: 1.3,
        ...style,
      }}
      {...rest}
    >
      {dot && <span style={{ width: 6, height: 6, borderRadius: "50%", background: t.dot, flex: "none" }} />}
      {children}
    </span>
  );
}
