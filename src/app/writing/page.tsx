export const metadata = {
  title: "Writing | Earned Conviction",
  description: "Essays and writing.",
};

export default function WritingPage() {
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
          <p>[List or grid of pieces can go here. Placeholder for now.]</p>
        </div>
      </section>
    </article>
  );
}
