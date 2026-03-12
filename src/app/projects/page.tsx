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
        <div className="max-w-2xl space-y-6 font-body text-foreground leading-relaxed">
          <p>[Overview of your projects and builders.]</p>
          <p>[Add project titles and short descriptions as you go.]</p>
        </div>
      </section>
    </article>
  );
}
