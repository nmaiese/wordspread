import React from "react";
import { Icon } from "./Icon";

/* DataLimitNote — inline ochre note for dataset limits. Honest, non-alarming. */

export interface DataLimitNoteProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
}

export function DataLimitNote({ children, title = "Stato del dataset", style = {}, ...rest }: DataLimitNoteProps) {
  return (
    <div
      style={{
        display: "flex",
        gap: 12,
        alignItems: "flex-start",
        padding: "14px 16px",
        background: "var(--ochre-50)",
        border: "1px solid var(--ochre-100)",
        borderRadius: "var(--radius-md)",
        ...style,
      }}
      {...rest}
    >
      <span style={{ color: "var(--ochre-700)", display: "flex", marginTop: 1, flex: "none" }}>
        <Icon name="info" size={18} />
      </span>
      <div style={{ minWidth: 0 }}>
        <div
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: 11,
            letterSpacing: "0.06em",
            textTransform: "uppercase",
            color: "var(--ochre-700)",
            fontWeight: 600,
            marginBottom: 3,
          }}
        >
          {title}
        </div>
        <div style={{ fontSize: 14, color: "var(--ink-700)", lineHeight: 1.5 }}>{children}</div>
      </div>
    </div>
  );
}
