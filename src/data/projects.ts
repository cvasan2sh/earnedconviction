export type ProjectStage = "0-1" | "1-10" | "10-100";
export type ProjectStatus = "active" | "building" | "paused";

export interface Project {
  slug: string;
  name: string;
  tagline: string;
  description: string;
  stage: ProjectStage;
  status: ProjectStatus;
  tags: string[];
  url?: string;
  github?: string;
}

export const projects: Project[] = [
  {
    slug: "innerloop",
    name: "InnerLoop",
    tagline: "AI-powered reflection and journaling",
    description:
      "A private thinking environment that helps you close open loops, surface patterns, and build self-knowledge over time.",
    stage: "0-1",
    status: "building",
    tags: ["AI", "productivity", "B2B SaaS"],
  },
  {
    slug: "zuari-farm-hub",
    name: "Zuari Farm Hub",
    tagline: "Agricultural intelligence for small farms",
    description:
      "A decision-support platform for smallholder farmers — crop planning, input optimization, market linkage.",
    stage: "0-1",
    status: "paused",
    tags: ["agritech", "emerging markets", "AI"],
  },
  {
    slug: "war-room",
    name: "War-Room",
    tagline: "Strategic simulation powered by The Forge",
    description:
      "A scenario planning and war-gaming tool built on The Forge deliberation system. For founders, operators, and strategists.",
    stage: "0-1",
    status: "building",
    tags: ["strategy", "The Forge", "B2B SaaS"],
  },
  {
    slug: "the-forge",
    name: "The Forge",
    tagline: "Multi-agent deliberation system",
    description:
      "Takes hard problems and subjects them to adversarial multi-perspective examination. Not an answer engine — a place where problems get tested under pressure until what remains is a conviction worth acting on or an honest map of irreducible uncertainty.",
    stage: "0-1",
    status: "active",
    tags: ["AI", "deliberation", "multi-agent"],
  },
];
