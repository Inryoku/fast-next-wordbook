import Link from "next/link";

import { fetchRecentWordsSSG, fetchTagsSSG } from "../lib/api";

export const dynamic = "force-static";

export default async function Home() {
  const [tags, words] = await Promise.all([fetchTagsSSG(), fetchRecentWordsSSG()]);

  return (
    <main className="page">
      <h1>Wordbook</h1>
      <p>FastAPI + Postgres + Next.js rendering strategies.</p>

      <section className="card" style={{ marginTop: "2rem" }}>
        <h2>Popular tags</h2>
        {tags.length === 0 ? (
          <p>No tags yet.</p>
        ) : (
          <ul>
            {tags.slice(0, 8).map((tag) => (
              <li key={tag.id}>
                <Link href={`/tags/${tag.slug}`}>{tag.label}</Link> ({tag.count})
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="card" style={{ marginTop: "2rem" }}>
        <h2>Recently added</h2>
        {words.items.length === 0 ? (
          <p>No words yet.</p>
        ) : (
          <ul>
            {words.items.map((word) => (
              <li key={word.id}>
                <Link href={`/words/${word.id}`}>{word.term}</Link> — {word.meaning}
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
