"use client";

import React from "react";
import { Icon } from "./Icon";

/* Input — text field with optional leading icon. Used heavily for search. */

export interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "size"> {
  iconLeft?: string;
  size?: "sm" | "md" | "lg";
  invalid?: boolean;
  containerStyle?: React.CSSProperties;
}

export function Input({
  iconLeft,
  size = "md",
  invalid = false,
  style = {},
  containerStyle = {},
  ...rest
}: InputProps) {
  const [focus, setFocus] = React.useState(false);
  const pad = size === "lg" ? "14px 16px" : size === "sm" ? "8px 12px" : "11px 14px";
  const fs = size === "lg" ? "17px" : size === "sm" ? "13px" : "15px";
  const iconSize = size === "lg" ? 20 : 17;
  const leftPad = iconLeft ? (size === "lg" ? 46 : 40) : undefined;

  return (
    <div style={{ position: "relative", display: "flex", alignItems: "center", width: "100%", ...containerStyle }}>
      {iconLeft && (
        <span
          style={{
            position: "absolute",
            left: size === "lg" ? 16 : 13,
            color: focus ? "var(--accent)" : "var(--text-faint)",
            display: "flex",
            pointerEvents: "none",
            transition: "color var(--dur-fast) var(--ease-out)",
          }}
        >
          <Icon name={iconLeft} size={iconSize} />
        </span>
      )}
      <input
        onFocus={(e) => {
          setFocus(true);
          rest.onFocus && rest.onFocus(e);
        }}
        onBlur={(e) => {
          setFocus(false);
          rest.onBlur && rest.onBlur(e);
        }}
        style={{
          width: "100%",
          padding: pad,
          paddingLeft: leftPad,
          fontSize: fs,
          fontFamily: "var(--font-ui)",
          color: "var(--text-strong)",
          background: "var(--surface-card)",
          border: `1.5px solid ${invalid ? "var(--danger)" : focus ? "var(--accent)" : "var(--border-strong)"}`,
          borderRadius: "var(--radius-md)",
          outline: "none",
          boxShadow: focus ? "var(--shadow-focus)" : "none",
          transition: "border-color var(--dur-fast) var(--ease-out), box-shadow var(--dur-fast) var(--ease-out)",
          ...style,
        }}
        {...rest}
      />
    </div>
  );
}
