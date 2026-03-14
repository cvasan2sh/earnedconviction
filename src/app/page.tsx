import Image from "next/image";
import { MDXRemote } from "next-mdx-remote/rsc";
import { getPageContent } from "@/lib/mdx";
import ContactForm from "@/components/ContactForm";
import SocialLinks from "./components/SocialLinks";

export default async function IdentityPage() {
  const { content, frontmatter } = await getPageContent("index");

  return (
    <article>
      {/* Hero: avatar + name + tagline */}
      <section className="pb-16">
        <div className="flex items-start gap-6 sm:gap-8">
          <Image
            src="/avatar.jpg"
            alt="Siva Pentakota"
            width={96}
            height={96}
            className="mt-1 shrink-0 rounded-full sm:h-28 sm:w-28"
            priority
          />
          <div>
            <h1 className="font-display text-3xl font-normal tracking-tight text-foreground sm:text-4xl md:text-5xl">
              {frontmatter.title as string}
            </h1>
            {frontmatter.description && (
              <p className="mt-3 font-body text-lg italic leading-relaxed text-muted sm:text-xl">
                {frontmatter.description as string}
              </p>
            )}
          </div>
        </div>
      </section>

      {/* Body: MDX content */}
      <div className="border-t border-accent pt-12">
        <div className="max-w-2xl space-y-5 font-body text-foreground leading-relaxed [&_h2]:font-display [&_h2]:text-2xl [&_h2]:mt-10 [&_h2]:mb-4 [&_p]:text-foreground/90 [&_strong]:text-foreground [&_a]:text-accent [&_a]:no-underline [&_a:hover]:underline">
          <MDXRemote source={content} />
        </div>
      </div>

      {/* Contact */}
      <section className="mt-16 border-t border-accent pt-12">
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
