import Link from "next/link";
import { projects } from "@/data/projects";

export const metadata = {
  title: "Projects | Earned Conviction",
  description: "What I'm building.",
};

export default function ProjectsPage() {
  return (
    <article>
      <section className="pb-24">
        <h1 className="font-display text-4xl font-normal tracking-tight text-foreground sm:text-5xl md:text-6xl">
          Projects
        </h1>
      </section>
      <section className="border-t border-accent pt-24">
        <ul className="list-none space-y-16 pl-0">
          {projects.map((project) => (
            <li key={project.slug} className="border-t border-accent pt-12 first:border-t-0 first:pt-0">
              <h2 className="font-display text-2xl font-normal text-foreground">
                {project.url ? (
                  <Link
                    href={project.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="no-underline text-foreground transition-colors hover:text-accent"
                  >
                    {project.name}
                    <span className="ml-2 text-base text-muted">↗</span>
                  </Link>
                ) : (
                  project.name
                )}
              </h2>
              <p className="mt-2 font-body text-foreground/90 leading-relaxed">
                {project.tagline}
              </p>
              <p className="mt-4 max-w-2xl font-body text-foreground/85 leading-relaxed">
                {project.description}
              </p>
              <div className="mt-4 flex flex-wrap items-center gap-2">
                <span
                  className="inline-block rounded px-2 py-0.5 font-body text-xs tracking-wide text-accent"
                  style={{ backgroundColor: "rgba(192, 57, 43, 0.15)" }}
                >
                  {project.stage}
                </span>
                <span className="font-body text-xs text-muted">
                  {project.status}
                </span>
                {!project.url && (
                  <span className="font-body text-xs italic text-muted">
                    Coming soon
                  </span>
                )}
                {project.tags.map((tag) => (
                  <span key={tag} className="font-body text-xs text-muted">
                    {tag}
                  </span>
                ))}
              </div>
            </li>
          ))}
        </ul>
      </section>
    </article>
  );
}
