import React from "react";
import { Icon } from "./Icon";

/* StateMessage — empty / loading / error / pending dataset states. A calm,
   centred message so missing data reads as a dataset status, not a bug. */

type Kind = "empty" | "loading" | "pending" | "error";

const KINDS: Record<Kind, { icon: string; color: string; ring: string }> = {
  empty: { icon: "search", color: "var(--text-muted)", ring: "var(--paper-sunk)" },
  loading: { icon: "loader", color: "var(--accent)", ring: "var(--teal-50)" },
  pending: { icon: "info", color: "var(--ochre-700)", ring: "var(--ochre-50)" },
  error: { icon: "alert-triangle", color: "var(--error-600)", ring: "var(--error-100)" },
};

export interface StateMessageProps extends React.HTMLAttributes<HTMLDivElement> {
  kind?: Kind;
  title?: string;
  description?: React.ReactNode;
  action?: React.ReactNode;
  compact?: boolean;
}

export function StateMessage({ kind = "empty", title, description, action, compact = false, style = {}, ...rest }: StateMessageProps) {
  const k = KINDS[kind] || KINDS.empty;
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        textAlign: "center",
        gap: 6,
        padding: compact ? "24px 20px" : "40px 24px",
        ...style,
      }}
      {...rest}
    >
      <span
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          width: 48,
          height: 48,
          borderRadius: "var(--radius-lg)",
          background: k.ring,
          color: k.color,
          marginBottom: 4,
        }}
      >
        <Icon name={k.icon} size={22} style={kind === "loading" ? { animation: "pm-spin 1s linear infinite" } : undefined} />
      </span>
      {title && <div style={{ fontSize: 16, fontWeight: 600, color: "var(--text-strong)" }}>{title}</div>}
      {description && <div style={{ fontSize: 14, color: "var(--text-muted)", maxWidth: 420, lineHeight: 1.5 }}>{description}</div>}
      {action && <div style={{ marginTop: 10 }}>{action}</div>}
    </div>
  );
}
