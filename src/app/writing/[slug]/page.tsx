import { MDXRemote } from "next-mdx-remote/rsc";
import Link from "next/link";
import { getAllWritingPosts, getWritingPost } from "@/lib/mdx";
import type { Metadata } from "next";

type Props = { params: Promise<{ slug: string }> };

export async function generateStaticParams() {
  const posts = await getAllWritingPosts();
  return posts.map((post) => ({ slug: post.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const { frontmatter } = await getWritingPost(slug);
  return {
    title: `${frontmatter.title as string} | Earned Conviction`,
    description: (frontmatter.description as string) ?? undefined,
  };
}

export default async function WritingPostPage({ params }: Props) {
  const { slug } = await params;
  const { content, frontmatter } = await getWritingPost(slug);

  return (
    <article>
      <div className="pb-24">
        <Link
          href="/writing"
          className="mb-8 inline-block font-body text-sm text-muted no-underline transition-colors hover:text-accent"
        >
          ← Writing
        </Link>
        <h1 className="font-display text-4xl font-normal tracking-tight text-foreground sm:text-5xl md:text-6xl">
          {frontmatter.title as string}
        </h1>
        <p className="mt-4 font-body text-muted">
          {frontmatter.date as string}
        </p>
      </div>
      <div className="border-t border-accent pt-24">
        <div className="max-w-2xl space-y-6 font-body text-foreground leading-relaxed [&_h1]:font-display [&_h1]:text-3xl [&_h2]:font-display [&_h2]:text-2xl [&_h2]:mt-12 [&_p]:text-foreground/90 [&_a]:text-accent [&_a]:no-underline [&_a:hover]:underline">
          <MDXRemote source={content} />
        </div>
      </div>
    </article>
  );
}
