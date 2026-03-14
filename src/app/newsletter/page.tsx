import NewsletterForm from "@/components/NewsletterForm";

export const metadata = {
  title: "Newsletter | Earned Conviction",
  description: "Subscribe to the newsletter.",
};

export default function NewsletterPage() {
  return (
    <article>
      <section className="pb-24">
        <h1 className="font-display text-4xl font-normal tracking-tight text-foreground sm:text-5xl md:text-6xl">
          Newsletter
        </h1>
        <p className="mt-8 max-w-2xl font-body text-xl leading-relaxed text-muted">
          Occasional writing on AI product building, enterprise SaaS, and ideas that survived The Forge.
        </p>
      </section>
      <section className="border-t border-accent pt-24">
        <div className="max-w-2xl space-y-6 font-body text-foreground leading-relaxed">
          <p className="text-foreground/90">
            No schedule. No filler. Just the thinking I'd want to read if someone else were writing it.
          </p>
          <NewsletterForm />
        </div>
      </section>
    </article>
  );
}
