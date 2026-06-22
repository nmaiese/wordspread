"use client";

import React from "react";
import { Icon } from "./Icon";

/* SourceLink — the recurring "fonte ufficiale" external link. Petrol, mono,
   with shield-check + external-link glyphs. The trust primitive of the product. */

export interface SourceLinkProps extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
  size?: "sm" | "md";
}

export function SourceLink({ href = "#", children = "Fonte ufficiale", size = "md", style = {}, ...rest }: SourceLinkProps) {
  const [hover, setHover] = React.useState(false);
  const fs = size === "sm" ? "12px" : "13px";
  return (
    <a
      href={href}
      target="_blank"
      rel="noreferrer"
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "5px",
        fontFamily: "var(--font-mono)",
        fontSize: fs,
        fontWeight: 500,
        color: "var(--accent)",
        textDecoration: hover ? "underline" : "none",
        textUnderlineOffset: "2px",
        letterSpacing: "0.01em",
        ...style,
      }}
      {...rest}
    >
      <Icon name="shield-check" size={size === "sm" ? 13 : 14} />
      {children}
      <Icon name="external-link" size={size === "sm" ? 12 : 13} style={{ opacity: 0.7 }} />
    </a>
  );
}
