"use client";

import React from "react";
import { Icon } from "./Icon";

/* Select — styled native select with chevron. */

export interface SelectProps extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, "size"> {
  size?: "sm" | "md" | "lg";
  containerStyle?: React.CSSProperties;
}

export function Select({ children, size = "md", style = {}, containerStyle = {}, ...rest }: SelectProps) {
  const [focus, setFocus] = React.useState(false);
  const pad =
    size === "lg" ? "14px 40px 14px 16px" : size === "sm" ? "8px 34px 8px 12px" : "11px 38px 11px 14px";
  const fs = size === "lg" ? "16px" : size === "sm" ? "13px" : "14px";
  return (
    <div style={{ position: "relative", display: "inline-flex", alignItems: "center", ...containerStyle }}>
      <select
        onFocus={() => setFocus(true)}
        onBlur={() => setFocus(false)}
        style={{
          appearance: "none",
          WebkitAppearance: "none",
          MozAppearance: "none",
          width: "100%",
          padding: pad,
          fontSize: fs,
          fontFamily: "var(--font-ui)",
          fontWeight: 500,
          color: "var(--text-strong)",
          background: "var(--surface-card)",
          border: `1.5px solid ${focus ? "var(--accent)" : "var(--border-strong)"}`,
          borderRadius: "var(--radius-md)",
          cursor: "pointer",
          outline: "none",
          boxShadow: focus ? "var(--shadow-focus)" : "none",
          transition: "border-color var(--dur-fast) var(--ease-out), box-shadow var(--dur-fast) var(--ease-out)",
          ...style,
        }}
        {...rest}
      >
        {children}
      </select>
      <span style={{ position: "absolute", right: 12, color: "var(--text-muted)", pointerEvents: "none", display: "flex" }}>
        <Icon name="chevron-down" size={16} />
      </span>
    </div>
  );
}
