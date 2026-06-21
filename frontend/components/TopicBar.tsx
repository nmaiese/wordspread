export function TopicBar({
  label,
  share,
  sub,
}: {
  label: string;
  share: number;
  sub?: string;
}) {
  const pct = Math.round(share * 100);
  return (
    <div className="topicbar">
      <div className="head">
        <span>{label}</span>
        <span className="muted">{pct}%{sub ? ` · ${sub}` : ""}</span>
      </div>
      <div className="track">
        <div className="fill" style={{ width: `${Math.max(2, pct)}%` }} />
      </div>
    </div>
  );
}
