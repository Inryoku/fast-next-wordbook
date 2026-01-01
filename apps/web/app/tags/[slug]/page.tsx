import Link from "next/link";

import { fetchTagDetailISR } from "../../../lib/api";

export const revalidate = 60;

export default async function TagDetailPage({
  params
}: {
  params: { slug: string };
}) {
  const data = await fetchTagDetailISR(params.slug);

  return (
    <main className="page">
      <h1>{data.tag.label}</h1>
      <p>{data.total} words</p>
      <section className="card" style={{ marginTop: "1.5rem" }}>
        <ul>
          {data.words.map((word) => (
            <li key={word.id}>
              <Link href={`/words/${word.id}`}>{word.term}</Link> — {word.meaning}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
