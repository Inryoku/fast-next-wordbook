import "./globals.css";
import type { Metadata } from "next";
import { Fraunces, Manrope } from "next/font/google";

const display = Fraunces({
  subsets: ["latin"],
  variable: "--font-display"
});
const body = Manrope({
  subsets: ["latin"],
  variable: "--font-body"
});

export const metadata: Metadata = {
  title: "next-fastapi-app",
  description: "Next.js + FastAPI monorepo"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${display.variable} ${body.variable}`}>
        <header className="site-header">
          <div className="nav-wrap">
            <a href="/" className="brand">
              Wordbook
            </a>
            <nav className="nav-links">
              <a href="/tags">Tags</a>
              <a href="/search?query=memory">Search</a>
              <a href="/search/stream?query=memory">Streaming</a>
              <a href="/study">Study</a>
            </nav>
          </div>
        </header>
        {children}
      </body>
    </html>
  );
}
