import { MDXRemote } from "next-mdx-remote/rsc";
import { getPageContent } from "@/lib/mdx";
import ContactForm from "@/components/ContactForm";

export async function generateMetadata() {
  const { frontmatter } = await getPageContent("about");
  return {
    title: `${frontmatter.title as string} | Earned Conviction`,
    description: frontmatter.description as string,
  };
}

export default async function AboutPage() {
  const { content } = await getPageContent("about");

  return (
    <article className="space-y-24">
      <div className="max-w-2xl space-y-8 font-body text-foreground leading-relaxed [&_h1]:font-display [&_h1]:text-4xl [&_h1]:tracking-tight [&_h2]:font-display [&_h2]:text-2xl [&_h2]:mt-16 [&_h2]:pt-8 [&_h2]:border-t [&_h2]:border-accent [&_p]:text-foreground/90 [&_a]:text-accent [&_a]:no-underline [&_a:hover]:underline">
        <MDXRemote source={content} components={{ ContactForm }} />
      </div>
    </article>
  );
}
