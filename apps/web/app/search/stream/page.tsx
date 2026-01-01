import { Suspense } from "react";

import { fetchTagsSSG, fetchWordsSSR } from "../../../lib/api";

export const dynamic = "force-dynamic";

async function TopMatches({ query }: { query: string }) {
  const results = await fetchWordsSSR(query);

  return (
    <section className="card">
      <h2>Top matches</h2>
      <ul>
        {results.items.slice(0, 5).map((word) => (
          <li key={word.id}>
            {word.term} — {word.meaning}
          </li>
        ))}
      </ul>
    </section>
  );
}

async function TagFacets() {
  const tags = await fetchTagsSSG();

  return (
    <section>
      <h2>Tag facets</h2>
      <ul>
        {tags.slice(0, 8).map((tag) => (
          <li key={tag.id}>
            {tag.label} ({tag.count})
          </li>
        ))}
      </ul>
    </section>
  );
}

export default async function SearchStreamPage({
  searchParams
}: {
  searchParams: { query?: string };
}) {
  const query = searchParams.query ?? "";

  return (
    <main className="page">
      <h1>Streaming search</h1>
      <p>Try: /search/stream?query=memory</p>

      {query ? (
        <div className="stack" style={{ marginTop: "1.5rem" }}>
          <Suspense fallback={<p>Loading top matches...</p>}>
            <TopMatches query={query} />
          </Suspense>
          <Suspense fallback={<p>Loading facets...</p>}>
            <section className="card">
              <TagFacets />
            </section>
          </Suspense>
        </div>
      ) : (
        <p style={{ marginTop: "1.5rem" }}>Enter a query to stream results.</p>
      )}
    </main>
  );
}
