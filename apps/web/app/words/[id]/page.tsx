import Link from "next/link";

import { fetchWordISR } from "../../../lib/api";

export const revalidate = 60;

export default async function WordDetailPage({
  params
}: {
  params: { id: string };
}) {
  const word = await fetchWordISR(params.id);

  return (
    <main className="page">
      <Link href="/">← Home</Link>
      <h1 style={{ marginTop: "1rem" }}>{word.term}</h1>
      <p>{word.meaning}</p>

      {word.tags.length > 0 && (
        <section className="card" style={{ marginTop: "1.5rem" }}>
          <h2>Tags</h2>
          <ul>
            {word.tags.map((tag) => (
              <li key={tag.id}>
                <Link href={`/tags/${tag.slug}`}>{tag.label}</Link>
              </li>
            ))}
          </ul>
        </section>
      )}

      {word.examples.length > 0 && (
        <section className="card" style={{ marginTop: "1.5rem" }}>
          <h2>Examples</h2>
          <ul>
            {word.examples.map((example) => (
              <li key={example.id}>
                “{example.sentence}”{example.source ? ` — ${example.source}` : ""}
              </li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
}
