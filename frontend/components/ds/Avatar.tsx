import React from "react";

/* Avatar — initials monogram. No photos in the dataset, so initials on a tinted
   ground; tone can mark comparison side (a/b). */

type Tone = "neutral" | "a" | "b" | "teal";

const TONES: Record<Tone, { bg: string; fg: string; bd: string }> = {
  neutral: { bg: "var(--paper-sunk)", fg: "var(--ink-700)", bd: "var(--line)" },
  a: { bg: "var(--coral-50)", fg: "var(--coral-700)", bd: "var(--coral-100)" },
  b: { bg: "var(--violet-50)", fg: "var(--violet-700)", bd: "var(--violet-100)" },
  teal: { bg: "var(--teal-50)", fg: "var(--teal-700)", bd: "var(--teal-100)" },
};

function initials(name = "") {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (!parts.length) return "—";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

export interface AvatarProps extends React.HTMLAttributes<HTMLSpanElement> {
  name?: string;
  size?: number;
  tone?: Tone;
}

export function Avatar({ name = "", size = 44, tone = "neutral", style = {}, ...rest }: AvatarProps) {
  const t = TONES[tone] || TONES.neutral;
  return (
    <span
      title={name}
      style={{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        width: size,
        height: size,
        flex: "none",
        borderRadius: "var(--radius-md)",
        background: t.bg,
        color: t.fg,
        border: `1px solid ${t.bd}`,
        fontFamily: "var(--font-mono)",
        fontWeight: 600,
        fontSize: Math.round(size * 0.36),
        letterSpacing: "0.01em",
        ...style,
      }}
      {...rest}
    >
      {initials(name)}
    </span>
  );
}
