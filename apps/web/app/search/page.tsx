import Link from "next/link";

import { fetchWordsSSR } from "../../lib/api";

export const dynamic = "force-dynamic";

export default async function SearchPage({
  searchParams
}: {
  searchParams: { query?: string; tag?: string; sort?: string };
}) {
  const query = searchParams.query ?? "";
  const tag = searchParams.tag;
  const sort = searchParams.sort ?? "new";

  const results = query ? await fetchWordsSSR(query, tag, sort) : { total: 0, items: [] };

  return (
    <main className="page">
      <h1>Search</h1>
      <p>Try: /search?query=memory</p>

      {query ? (
        <section className="card" style={{ marginTop: "1.5rem" }}>
          <p>
            {results.total} result{results.total === 1 ? "" : "s"} for "{query}"
          </p>
          <ul>
            {results.items.map((word) => (
              <li key={word.id}>
                <Link href={`/words/${word.id}`}>{word.term}</Link> — {word.meaning}
              </li>
            ))}
          </ul>
        </section>
      ) : (
        <p style={{ marginTop: "1.5rem" }}>Enter a query to see results.</p>
      )}
    </main>
  );
}
