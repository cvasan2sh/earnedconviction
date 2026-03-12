import Link from "next/link";

export default function Home() {
  return (
    <article>
      <section className="pb-24">
        <h1 className="font-display text-4xl font-normal tracking-tight text-foreground sm:text-5xl md:text-7xl">
          Siva Pentakota
        </h1>
        <p className="mt-8 font-body text-xl italic leading-relaxed text-muted">
          [One line: what you do and believe. Replace this placeholder.]
        </p>
      </section>

      <section className="border-t border-accent pt-24">
        <h2 className="font-display text-2xl font-normal text-foreground">
          What I&apos;m Building
        </h2>
        <p className="mt-6 max-w-2xl font-body text-foreground leading-relaxed">
          [Short intro to your projects. One or two sentences.]
        </p>
        <p className="mt-6">
          <Link
            href="/projects"
            className="font-body text-foreground/90 no-underline transition-colors hover:text-accent"
          >
            View projects →
          </Link>
        </p>
      </section>

      <section className="border-t border-accent pt-24">
        <h2 className="font-display text-2xl font-normal text-foreground">
          How I Think
        </h2>
        <p className="mt-6 max-w-2xl font-body text-foreground leading-relaxed">
          [One or two sentences on your methodology and first principles.]
        </p>
        <p className="mt-6">
          <Link
            href="/forge"
            className="font-body text-foreground/90 no-underline transition-colors hover:text-accent"
          >
            The Forge →
          </Link>
        </p>
      </section>

      <section className="border-t border-accent pt-24">
        <h2 className="font-display text-2xl font-normal text-foreground">
          What I&apos;m Writing
        </h2>
        <p className="mt-6 max-w-2xl font-body text-foreground leading-relaxed">
          [Teaser for your latest writing.]
        </p>
        <p className="mt-6">
          <Link
            href="/writing"
            className="font-body text-foreground/90 no-underline transition-colors hover:text-accent"
          >
            Latest writing →
          </Link>
        </p>
      </section>
    </article>
  );
}
