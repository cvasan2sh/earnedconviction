import Avatar from "../components/Avatar";
import SocialLinks from "../components/SocialLinks";

export const metadata = {
  title: "About | Earned Conviction",
  description: "About Siva Pentakota.",
};

export default function AboutPage() {
  return (
    <article>
      <section className="pb-24">
        <h1 className="font-display text-4xl font-normal tracking-tight text-foreground sm:text-5xl md:text-6xl">
          About
        </h1>
      </section>
      <section className="border-t border-accent pt-24">
        <div className="space-y-12">
          <div className="space-y-8">
            <div className="flex justify-start">
              <Avatar size={160} initials="SP" />
            </div>
            <SocialLinks variant="iconText" />
          </div>

          <div className="max-w-2xl space-y-6 font-body text-foreground leading-relaxed">
          <p>[Your story, background, and what drives you. Fill in.]</p>
          <p>[Second paragraph.]</p>
          <p>[Third paragraph if needed.]</p>
          </div>
        </div>
      </section>
    </article>
  );
}
