import React from "react";

/* Tag / Chip — keyword & topic token. Optional removable. */

type Tone = "neutral" | "teal" | "a" | "b";

export interface TagProps extends React.HTMLAttributes<HTMLSpanElement> {
  tone?: Tone;
  active?: boolean;
  onRemove?: () => void;
}

export function Tag({ children, tone = "neutral", onRemove, active = false, style = {}, ...rest }: TagProps) {
  const tones: Record<Tone, { bg: string; fg: string; bd: string }> = {
    neutral: {
      bg: active ? "var(--ink-900)" : "var(--paper-sunk)",
      fg: active ? "#fff" : "var(--ink-700)",
      bd: active ? "var(--ink-900)" : "var(--line)",
    },
    teal: { bg: "var(--teal-50)", fg: "var(--teal-700)", bd: "var(--teal-100)" },
    a: { bg: "var(--coral-50)", fg: "var(--coral-700)", bd: "var(--coral-100)" },
    b: { bg: "var(--violet-50)", fg: "var(--violet-700)", bd: "var(--violet-100)" },
  };
  const t = tones[tone] || tones.neutral;
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "6px",
        padding: "4px 10px",
        fontSize: "13px",
        fontFamily: "var(--font-ui)",
        fontWeight: 500,
        color: t.fg,
        background: t.bg,
        border: `1px solid ${t.bd}`,
        borderRadius: "var(--radius-sm)",
        lineHeight: 1.3,
        ...style,
      }}
      {...rest}
    >
      {children}
      {onRemove && (
        <button
          onClick={onRemove}
          aria-label="Rimuovi"
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            border: "none",
            background: "transparent",
            cursor: "pointer",
            color: "inherit",
            opacity: 0.6,
            padding: 0,
            marginRight: -2,
            fontSize: 14,
            lineHeight: 1,
          }}
        >
          ×
        </button>
      )}
    </span>
  );
}
