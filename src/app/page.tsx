import Link from "next/link";
import { projects } from "@/data/projects";

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
        <ul className="mt-8 list-none space-y-12 pl-0">
          {projects.map((project) => (
            <li key={project.slug}>
              <h3 className="font-display text-xl font-normal text-foreground">
                {project.name}
              </h3>
              <p className="mt-1 font-body text-foreground/90 leading-relaxed">
                {project.tagline}
              </p>
              <div className="mt-3 flex flex-wrap items-center gap-2">
                <span
                  className="inline-block rounded px-2 py-0.5 font-body text-xs tracking-wide text-accent"
                  style={{ backgroundColor: "rgba(192, 57, 43, 0.15)" }}
                >
                  {project.stage}
                </span>
                <span className="font-body text-xs text-muted">
                  {project.status}
                </span>
                {project.tags.map((tag) => (
                  <span key={tag} className="font-body text-xs text-muted">
                    {tag}
                  </span>
                ))}
              </div>
            </li>
          ))}
        </ul>
        <p className="mt-8">
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
