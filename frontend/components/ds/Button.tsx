"use client";

import React from "react";
import { Icon } from "./Icon";

/* Button — primary action control. Variants: primary, secondary, ghost, danger. */

const SIZES: Record<string, { padding: string; fontSize: string; gap: string; icon: number }> = {
  sm: { padding: "7px 12px", fontSize: "13px", gap: "6px", icon: 15 },
  md: { padding: "10px 16px", fontSize: "14px", gap: "8px", icon: 17 },
  lg: { padding: "13px 22px", fontSize: "16px", gap: "9px", icon: 19 },
};

const VARIANTS: Record<string, React.CSSProperties> = {
  primary: { background: "var(--accent)", color: "var(--text-on-accent)", border: "1px solid var(--accent)" },
  secondary: { background: "var(--surface-card)", color: "var(--text-strong)", border: "1px solid var(--border-strong)" },
  ghost: { background: "transparent", color: "var(--text-body)", border: "1px solid transparent" },
  danger: { background: "var(--danger)", color: "#fff", border: "1px solid var(--danger)" },
};

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  iconLeft?: string;
  iconRight?: string;
  fullWidth?: boolean;
}

export function Button({
  children,
  variant = "primary",
  size = "md",
  iconLeft,
  iconRight,
  disabled = false,
  fullWidth = false,
  type = "button",
  style = {},
  ...rest
}: ButtonProps) {
  const s = SIZES[size] || SIZES.md;
  const v = VARIANTS[variant] || VARIANTS.primary;
  const [hover, setHover] = React.useState(false);

  const hoverStyle: React.CSSProperties =
    !disabled && hover
      ? variant === "primary"
        ? { background: "var(--accent-hover)", borderColor: "var(--accent-hover)" }
        : variant === "secondary"
        ? { background: "var(--surface-hover)" }
        : variant === "ghost"
        ? { background: "var(--accent-tint)", color: "var(--accent-hover)" }
        : { filter: "brightness(0.94)" }
      : {};

  return (
    <button
      type={type}
      disabled={disabled}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        gap: s.gap,
        padding: s.padding,
        fontSize: s.fontSize,
        fontFamily: "var(--font-ui)",
        fontWeight: 600,
        lineHeight: 1.1,
        borderRadius: "var(--radius-md)",
        cursor: disabled ? "not-allowed" : "pointer",
        width: fullWidth ? "100%" : "auto",
        opacity: disabled ? 0.5 : 1,
        transition:
          "background var(--dur-fast) var(--ease-out), color var(--dur-fast) var(--ease-out), border-color var(--dur-fast) var(--ease-out)",
        ...v,
        ...hoverStyle,
        ...style,
      }}
      {...rest}
    >
      {iconLeft && <Icon name={iconLeft} size={s.icon} />}
      {children}
      {iconRight && <Icon name={iconRight} size={s.icon} />}
    </button>
  );
}
