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
      </section>
      <section className="border-t border-accent pt-24">
        <div className="max-w-2xl space-y-6 font-body text-foreground leading-relaxed">
          <p>[What readers get. How often. Why they should sign up.]</p>
          <p>[Placeholder for signup form or link to your provider.]</p>
        </div>
      </section>
    </article>
  );
}
