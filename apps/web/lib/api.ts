import type { SearchResponse, TagDetail, TagWithCount, Word, WordList } from "./types";

const API_BASE_URL = process.env.API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";

async function apiFetch<T>(
  path: string,
  init?: RequestInit,
  nextConfig?: { revalidate?: number; cache?: RequestCache }
): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    cache: nextConfig?.cache,
    next: nextConfig?.revalidate ? { revalidate: nextConfig.revalidate } : undefined
  });

  if (!res.ok) {
    throw new Error(`API error ${res.status} for ${path}`);
  }
  return res.json() as Promise<T>;
}

export function fetchTagsSSG() {
  return apiFetch<TagWithCount[]>("/tags", undefined, { cache: "force-cache" });
}

export function fetchTagDetailISR(slug: string, page = 0) {
  const params = new URLSearchParams({ skip: String(page * 20), limit: "20" });
  return apiFetch<TagDetail>(`/tags/${slug}?${params.toString()}`, undefined, {
    revalidate: 60
  });
}

export function fetchWordsSSR(query: string, tag?: string, sort = "new") {
  const params = new URLSearchParams({ q: query, sort });
  if (tag) params.set("tag", tag);
  return apiFetch<SearchResponse>(`/search?${params.toString()}`, undefined, {
    cache: "no-store"
  });
}

export function fetchWordISR(id: string) {
  return apiFetch<Word>(`/words/${id}`, undefined, { revalidate: 60 });
}

export function fetchRecentWordsSSG() {
  const params = new URLSearchParams({ skip: "0", limit: "10", sort: "new" });
  return apiFetch<WordList>(`/words?${params.toString()}`, undefined, { cache: "force-cache" });
}
