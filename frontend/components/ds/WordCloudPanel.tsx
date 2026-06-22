import React from "react";

/* WordCloudPanel — identity element inherited from Wordspread, not the centre.
   Font size scales with score; petrol ink. Items: { keyword, score }. */

export interface WordCloudItem {
  keyword: string;
  score: number;
}

export interface WordCloudPanelProps extends React.HTMLAttributes<HTMLDivElement> {
  items: WordCloudItem[];
  max?: number;
}

export function WordCloudPanel({ items = [], max = 36, style = {}, ...rest }: WordCloudPanelProps) {
  const top = items.slice(0, max);
  if (!top.length) {
    return (
      <div style={{ color: "var(--text-muted)", fontSize: 14, fontStyle: "italic", ...style }}>
        Nessuna keyword disponibile.
      </div>
    );
  }
  const scores = top.map((i) => i.score);
  const hi = Math.max(...scores) || 1;
  const lo = Math.min(...scores);
  const norm = (s: number) => (s - lo) / (hi - lo || 1);
  const size = (s: number) => 14 + Math.round(norm(s) * 26);
  const weight = (s: number) => (norm(s) > 0.6 ? 600 : norm(s) > 0.3 ? 500 : 400);
  const color = (s: number) => {
    const n = norm(s);
    return n > 0.66 ? "var(--teal-700)" : n > 0.33 ? "var(--teal-600)" : "var(--ink-500)";
  };
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: "6px 18px", alignItems: "baseline", ...style }} {...rest}>
      {top.map((i) => (
        <span
          key={i.keyword}
          title={`score ${Number(i.score).toFixed(3)}`}
          style={{
            fontFamily: "var(--font-serif)",
            fontSize: size(i.score),
            fontWeight: weight(i.score),
            color: color(i.score),
            lineHeight: 1.1,
          }}
        >
          {i.keyword}
        </span>
      ))}
    </div>
  );
}
