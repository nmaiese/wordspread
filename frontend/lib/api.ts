// Client tipizzato verso l'API di Parla Mente.

export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

export interface PoliticianSummary {
  id: string;
  full_name: string;
  chamber: string;
  group_name: string | null;
  legislature: string;
}

export interface EvidenceItem {
  date: string;
  source: string;
  document_type: string;
  title: string;
  quote: string;
  url: string;
  entity_type: string;
  score: number;
}

export interface TopicEvidence {
  topic: string;
  topic_id: string;
  macro_area: string;
  score: number;
  intervention_count: number;
  act_count: number;
  keywords: string[];
  evidence: EvidenceItem[];
}

export interface Profile {
  politician: PoliticianSummary & { official_url: string | null };
  kpi: {
    intervention_count: number;
    act_count: number;
    topic_count: number;
    period: { from: string | null; to: string | null };
  };
  top_topics: {
    topic_id: string;
    topic: string;
    macro_area: string;
    share: number;
    intervention_count: number;
    act_count: number;
    keywords: string[];
  }[];
  timeline: Record<string, number | string>[];
  keywords: { keyword: string; score: number; frequency: number }[];
  evidence: TopicEvidence[];
  interventions: {
    id: string;
    date: string | null;
    context: string;
    text: string;
    source_url: string;
  }[];
  acts: {
    id: string;
    date: string | null;
    act_type: string;
    title: string;
    status: string | null;
    source_url: string;
  }[];
}

async function getJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`API ${path} -> ${res.status}`);
  return res.json();
}

export function searchPoliticians(params: {
  q?: string;
  chamber?: string;
  legislature?: string;
  limit?: number;
}): Promise<PoliticianSummary[]> {
  const qs = new URLSearchParams();
  if (params.q) qs.set("q", params.q);
  if (params.chamber) qs.set("chamber", params.chamber);
  if (params.legislature) qs.set("legislature", params.legislature);
  qs.set("limit", String(params.limit ?? 50));
  return getJSON(`/politicians?${qs.toString()}`);
}

export function getProfile(id: string): Promise<Profile> {
  return getJSON(`/politicians/${id}`);
}

export function compare(a: string, b: string): Promise<any> {
  return getJSON(`/compare?a=${encodeURIComponent(a)}&b=${encodeURIComponent(b)}`);
}
