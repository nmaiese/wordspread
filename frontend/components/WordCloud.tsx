"use client";

// Word cloud "leggera": elemento identitario ereditato da Wordspread, reso con CSS
// (dimensione del font proporzionale allo score). Non è il centro dell'app — lo è
// la mappa tematica verificabile — ma resta come firma visiva.

export function WordCloud({
  items,
  max = 40,
}: {
  items: { keyword: string; score: number }[];
  max?: number;
}) {
  const top = items.slice(0, max);
  if (top.length === 0) return <p className="muted">Nessuna keyword disponibile.</p>;
  const hi = Math.max(...top.map((i) => i.score)) || 1;
  const lo = Math.min(...top.map((i) => i.score));
  const size = (s: number) => 13 + Math.round(((s - lo) / (hi - lo || 1)) * 26);
  const opacity = (s: number) => 0.55 + ((s - lo) / (hi - lo || 1)) * 0.45;
  return (
    <div className="cloud">
      {top.map((i) => (
        <span
          key={i.keyword}
          style={{ fontSize: size(i.score), opacity: opacity(i.score) }}
          title={`score ${i.score.toFixed(3)}`}
        >
          {i.keyword}
        </span>
      ))}
    </div>
  );
}
