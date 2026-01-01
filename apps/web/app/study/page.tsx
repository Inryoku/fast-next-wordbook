"use client";

import { useEffect, useState } from "react";

const STORAGE_KEY = "wordbook-study-session";

export default function StudyPage() {
  const [today, setToday] = useState<string[]>([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (raw) {
      try {
        setToday(JSON.parse(raw));
      } catch {
        setToday([]);
      }
    }
  }, []);

  useEffect(() => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(today));
  }, [today]);

  return (
    <main className="page">
      <h1>Study session</h1>
      <p>Local-only list stored in localStorage.</p>

      <form
        className="card"
        onSubmit={(event) => {
          event.preventDefault();
          if (!input.trim()) return;
          setToday((prev) => [...prev, input.trim()]);
          setInput("");
        }}
      >
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Add a word"
          />
          <button type="submit">Add</button>
        </div>
      </form>

      <section className="card" style={{ marginTop: "1.5rem" }}>
        <ul>
          {today.map((item, index) => (
            <li key={`${item}-${index}`}>{item}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}
