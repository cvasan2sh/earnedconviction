import Image from "next/image";
import { MDXRemote } from "next-mdx-remote/rsc";
import { getPageContent } from "@/lib/mdx";
import ContactForm from "@/components/ContactForm";
import SocialLinks from "./components/SocialLinks";

export default async function IdentityPage() {
  const { content, frontmatter } = await getPageContent("index");

  return (
    <article>
      <section className="pb-24">
        <Image
          src="/avatar.jpg"
          alt="Siva Pentakota"
          width={120}
          height={120}
          className="mb-10 rounded-full"
          priority
        />
        <h1 className="font-display text-4xl font-normal tracking-tight text-foreground sm:text-5xl md:text-7xl">
          {frontmatter.title as string}
        </h1>
        {frontmatter.description && (
          <p className="mt-8 font-body text-xl italic leading-relaxed text-muted">
            {frontmatter.description as string}
          </p>
        )}
      </section>

      <div className="border-t border-accent pt-24">
        <div className="max-w-2xl space-y-6 font-body text-foreground leading-relaxed [&_h2]:font-display [&_h2]:text-2xl [&_h2]:mt-12 [&_h2]:pt-12 [&_h2]:border-t [&_h2]:border-accent [&_p]:text-foreground/90 [&_strong]:text-foreground [&_a]:text-accent [&_a]:no-underline [&_a:hover]:underline">
          <MDXRemote source={content} />
        </div>
      </div>

      <section className="mt-12 border-t border-accent pt-12">
        <h2 className="font-display text-2xl font-normal text-foreground">
          Send me a message
        </h2>
        <div className="mt-8">
          <ContactForm />
        </div>
        <div className="mt-12">
          <SocialLinks variant="iconText" />
        </div>
      </section>
    </article>
  );
}
