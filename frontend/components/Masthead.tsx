"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Badge } from "@/components/ds";

/* Masthead — sticky editorial header: serif wordmark + petrol dot, nav, phase badge. */

function NavLink({ href, label, active }: { href: string; label: string; active: boolean }) {
  return (
    <Link
      href={href}
      style={{
        textDecoration: "none",
        padding: "6px 2px",
        fontFamily: "var(--font-ui)",
        fontSize: 14.5,
        fontWeight: active ? 600 : 500,
        color: active ? "var(--ink-900)" : "var(--ink-500)",
        borderBottom: active ? "2px solid var(--teal-600)" : "2px solid transparent",
      }}
    >
      {label}
    </Link>
  );
}

export function Masthead() {
  const pathname = usePathname() || "/";
  const onCompare = pathname.startsWith("/compare");
  const onHome = !onCompare;
  return (
    <header
      style={{
        borderBottom: "1px solid var(--border)",
        background: "color-mix(in srgb, var(--paper) 80%, white)",
        backdropFilter: "blur(6px)",
        position: "sticky",
        top: 0,
        zIndex: 20,
      }}
    >
      <div
        style={{
          maxWidth: "var(--content-max)",
          margin: "0 auto",
          padding: "0 var(--gutter)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          height: 64,
        }}
      >
        <Link href="/" style={{ display: "flex", alignItems: "baseline", gap: 10, textDecoration: "none" }}>
          <span style={{ fontFamily: "var(--font-serif)", fontWeight: 600, fontSize: 23, letterSpacing: "-0.02em", color: "var(--ink-900)" }}>
            Parla Mente
          </span>
          <span style={{ width: 7, height: 7, borderRadius: "50%", background: "var(--teal-600)", display: "inline-block" }} />
        </Link>
        <nav style={{ display: "flex", gap: 22, alignItems: "center" }}>
          <NavLink href="/" label="Cerca" active={onHome} />
          <NavLink href="/compare" label="Confronta" active={onCompare} />
          <Badge tone="verify" dot size="sm">
            Fase 1 · Camera
          </Badge>
        </nav>
      </div>
    </header>
  );
}
