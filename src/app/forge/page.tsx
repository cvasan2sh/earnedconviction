export const metadata = {
  title: "The Forge | Earned Conviction",
  description: "Methodology and first principles.",
};

export default function ForgePage() {
  return (
    <article className="space-y-24">
      <header className="pb-24">
        <h1 className="font-display text-4xl font-normal tracking-tight text-foreground sm:text-5xl md:text-6xl">
          The Forge
        </h1>
        <p className="mt-8 max-w-2xl font-body text-xl text-foreground/90 leading-relaxed">
          [One paragraph: what this page is. The place where ideas are tested,
          refined, and made permanent. Your methodology in your words.]
        </p>
      </header>

      <section className="space-y-8 border-t border-accent pt-24">
        <h2 className="font-display text-2xl font-normal text-foreground">
          Methodology
        </h2>
        <div className="max-w-2xl space-y-6 font-body text-foreground/90 leading-relaxed">
          <p>
            [How you think. How you separate signal from noise. How you update.
            One or two paragraphs.]
          </p>
          <p>[Second paragraph if needed.]</p>
        </div>
      </section>

      <section className="border-t border-accent pt-24">
        <h2 className="font-display text-2xl font-normal text-foreground">
          The First Principles
        </h2>
        <ul className="mt-12 list-none space-y-0 pl-0">
          <li className="border-l-2 border-accent py-8 pl-8 first:pt-0">
            <p className="font-body italic leading-relaxed text-foreground/90">
              [First principle. One or two sentences. Replace with your own.]
            </p>
          </li>
          <li className="border-l-2 border-accent py-8 pl-8">
            <p className="font-body italic leading-relaxed text-foreground/90">
              [Second principle.]
            </p>
          </li>
          <li className="border-l-2 border-accent py-8 pl-8">
            <p className="font-body italic leading-relaxed text-foreground/90">
              [Third principle.]
            </p>
          </li>
          <li className="border-l-2 border-accent py-8 pl-8">
            <p className="font-body italic leading-relaxed text-foreground/90">
              [Fourth principle.]
            </p>
          </li>
          <li className="border-l-2 border-accent py-8 pl-8">
            <p className="font-body italic leading-relaxed text-foreground/90">
              [Fifth principle. Add or remove items as you like.]
            </p>
          </li>
        </ul>
      </section>
    </article>
  );
}
