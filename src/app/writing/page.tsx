import Link from "next/link";
import { getAllWritingPosts } from "@/lib/mdx";

export const metadata = {
  title: "Writing | Earned Conviction",
  description: "Essays and writing.",
};

export default async function WritingPage() {
  const posts = await getAllWritingPosts();

  return (
    <article>
      <section className="pb-24">
        <h1 className="font-display text-4xl font-normal tracking-tight text-foreground sm:text-5xl md:text-6xl">
          Writing
        </h1>
      </section>
      <section className="border-t border-accent pt-24">
        <div className="max-w-2xl space-y-6 font-body text-foreground leading-relaxed">
          <p>[Intro to your writing. What you write about and why.]</p>
        </div>
        <ul className="mt-16 list-none space-y-16 pl-0">
          {posts.map((post) => (
            <li key={post.slug} className="border-t border-accent pt-12">
              <Link
                href={`/writing/${post.slug}`}
                className="block no-underline"
              >
                <h2 className="font-display text-2xl font-normal text-foreground transition-colors hover:text-accent">
                  {post.title}
                </h2>
                <p className="mt-2 font-body text-sm text-muted">{post.date}</p>
                <p className="mt-2 font-body text-foreground/90 leading-relaxed">
                  {post.description}
                </p>
                <div className="mt-4 flex flex-wrap items-center gap-3">
                  {post.stage && (
                    <span
                      className="inline-block rounded px-2 py-0.5 font-body text-xs tracking-wide text-accent"
                      style={{ backgroundColor: "rgba(192, 57, 43, 0.15)" }}
                    >
                      {post.stage}
                    </span>
                  )}
                  {post.tags.map((tag) => (
                    <span
                      key={tag}
                      className="font-body text-xs text-muted"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </article>
  );
}
