import Link from "next/link";

import { fetchTagsSSG } from "../../lib/api";

export const dynamic = "force-static";

export default async function TagsPage() {
  const tags = await fetchTagsSSG();

  return (
    <main className="page">
      <h1>Tags</h1>
      <section className="card" style={{ marginTop: "1.5rem" }}>
        {tags.length === 0 ? (
          <p>No tags yet.</p>
        ) : (
          <ul>
            {tags.map((tag) => (
              <li key={tag.id}>
                <Link href={`/tags/${tag.slug}`}>{tag.label}</Link> ({tag.count})
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
