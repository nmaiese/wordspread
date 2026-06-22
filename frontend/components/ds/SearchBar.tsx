"use client";

import React from "react";
import { Input } from "./Input";
import { Select } from "./Select";
import { Button } from "./Button";

/* SearchBar — the prominent entry point: big search field + chamber / legislature
   / group filters. Presentational; wire value/onChange from the host. */

export interface SearchBarProps {
  value?: string;
  onChange?: (v: string) => void;
  onSubmit?: () => void;
  chamber?: string;
  onChamberChange?: (v: string) => void;
  legislature?: string;
  onLegislatureChange?: (v: string) => void;
  group?: string;
  onGroupChange?: (v: string) => void;
  groups?: string[];
  placeholder?: string;
  style?: React.CSSProperties;
}

export function SearchBar({
  value = "",
  onChange,
  onSubmit,
  chamber = "",
  onChamberChange,
  legislature = "19",
  onLegislatureChange,
  group = "",
  onGroupChange,
  groups = [],
  placeholder = "Cerca un deputato o senatore per nome…",
  style = {},
}: SearchBarProps) {
  return (
    <div style={{ ...style }}>
      <div style={{ display: "flex", gap: 10, alignItems: "stretch", flexWrap: "wrap" }}>
        <div style={{ flex: "1 1 320px", minWidth: 0 }}>
          <Input
            iconLeft="search"
            size="lg"
            value={value}
            placeholder={placeholder}
            onChange={(e) => onChange && onChange(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && onSubmit) onSubmit();
            }}
          />
        </div>
        <Button size="lg" iconLeft="search" onClick={onSubmit}>
          Cerca
        </Button>
      </div>

      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 12, alignItems: "center" }}>
        <span
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 6,
            fontFamily: "var(--font-mono)",
            fontSize: 11,
            letterSpacing: "0.06em",
            textTransform: "uppercase",
            color: "var(--text-faint)",
            marginRight: 2,
          }}
        >
          Filtri
        </span>
        <Select value={chamber} onChange={(e) => onChamberChange && onChamberChange(e.target.value)}>
          <option value="">Camera e Senato</option>
          <option value="camera">Camera</option>
          <option value="senato">Senato</option>
        </Select>
        <Select value={legislature} onChange={(e) => onLegislatureChange && onLegislatureChange(e.target.value)}>
          <option value="19">Legislatura 19</option>
          <option value="18">Legislatura 18</option>
        </Select>
        <Select value={group} onChange={(e) => onGroupChange && onGroupChange(e.target.value)}>
          <option value="">Tutti i gruppi</option>
          {groups.map((g) => (
            <option key={g} value={g}>
              {g}
            </option>
          ))}
        </Select>
      </div>
    </div>
  );
}
