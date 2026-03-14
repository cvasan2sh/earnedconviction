# PRD — earnedconviction.com Website

---
version: 1.1
last_updated: 2026-03-14
updated_by: Siva Pentakota
change: Simplified structure — killed Home and About, merged into root Identity page. Moved The Forge into Projects. Four pages only.
---

---

## What This Is

earnedconviction.com is Siva Pentakota's personal home on the internet. Three things simultaneously:

- A personal brand and professional identity
- The public home of The Forge — a multi-agent deliberation system
- A publishing platform that turns deliberation into domain-authority content

The methodology is the brand. The brand is the person. The content is the proof.

---

## Design Brief

Feels like the best book you ever read — if it had been designed by Apple. Every element earns its place or gets removed.

---

## Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Framework | Next.js App Router + TypeScript | Static generation |
| Styling | Tailwind CSS | Design system via CSS variables in globals.css |
| Hosting | Vercel free tier | Auto-deploys on push to main |
| DNS | Cloudflare | Free email routing |
| Content | MDX files in src/content/ | Git is version history. No CMS. |
| Newsletter | Resend free tier | 3,000 emails/month |
| Email | siva@earnedconviction.com | Cloudflare routing → Gmail |
| Repo | github.com/cvasan2sh/earnedconviction | main = production |

Total monthly cost: zero.

---

## Design System — Never Violate

| Token | Value |
|-------|-------|
| Background | #1A1A1A |
| Text | #F5F0E8 |
| Accent | #C0392B |
| Display font | Playfair Display |
| Body font | Source Serif 4 |

Prohibitions:
- No hero sections with CTA buttons
- No card grids
- No purple gradients
- No decorative elements that don't serve the thinking
- One animation per page maximum

---

## Site Structure — Four Pages Only

| Page | URL | Purpose |
|------|-----|---------|
| Identity | / | Who Siva is — story, work, beliefs, CV, socials. Replaces Home + About. |
| Writing | /writing | All deliberations, essays, whitepapers, GEO explainers |
| Projects | /projects | InnerLoop, Zuari, War-Room, The Forge |
| Newsletter | /newsletter | Single signup, Resend powered |

Nav: About (→ /), Writing, Projects, Newsletter

---

## Page Specs

### / — Identity Page
One page, one scroll. Sections:
1. Name — "Siva Pentakota" large in Playfair Display
2. One-line identity
3. Human story — career arc, transition from enterprise SaaS to AI product building
4. What he's building — project list linking to /projects
5. How he thinks — brief Forge description linking to its project card
6. CV / experience
7. Socials — LinkedIn, Twitter/X, GitHub

Content: `src/content/pages/index.mdx`

### /writing
Lists all MDX articles ordered by date descending.
Shows per article: title, date, description, tags, stage.
Individual article at `/writing/[slug]`.

### /projects
Driven entirely by `src/data/projects.ts`.

| Project | Description | Status |
|---------|-------------|--------|
| The Forge | Multi-agent deliberation system | Active |
| InnerLoop | AI-powered reflection and journaling | Building |
| Zuari Farm Hub | Agricultural market intelligence | Live |
| War-Room | Sales intelligence and deal review | Live |

Note: Zuari and War-Room use Bloomberg terminal aesthetic. Projects can have their own design language — same philosophy, different execution.

### /newsletter
Single email signup. Powered by Resend.
From: siva@earnedconviction.com

---

## File Structure

```
earnedconviction/
├── _cowork/
│   ├── PRD-site.md          ← this file
│   ├── PRD-forge.md         ← The Forge system PRD
│   ├── CONTEXT.md
│   ├── CONVENTIONS.md
│   └── TASKS.md
├── forge-sessions/
│   ├── _template.md
│   └── YYYY-MM/
├── public/
│   ├── avatar.jpg
│   ├── favicon.svg
│   └── logo.svg
└── src/
    ├── app/
    │   ├── writing/[slug]/
    │   ├── projects/
    │   ├── newsletter/
    │   ├── api/contact/
    │   ├── components/
    │   ├── globals.css
    │   ├── layout.tsx
    │   └── page.tsx          ← Identity page
    ├── components/
    ├── content/
    │   ├── pages/
    │   │   └── index.mdx     ← Identity page content
    │   └── writing/          ← YYYY-MM-DD-slug.mdx
    ├── data/
    │   └── projects.ts
    └── lib/
        └── mdx.ts
```

Deleted from original scaffold:
- src/app/about/ — merged into root
- src/app/forge/ — moved to projects
- src/content/pages/about.mdx — replaced by index.mdx
- src/content/pages/forge.mdx — content moved to projects.ts

---

## Conventions

### New article
1. Create `src/content/writing/YYYY-MM-DD-slug.mdx`
2. Frontmatter:
```yaml
---
title:
date: YYYY-MM-DD
description: One sentence
tags: []
stage: 0-1 | 1-10 | 10-100
agents: []
---
```
3. Push to main → live in 60 seconds

### New project
1. Edit `src/data/projects.ts`
2. Fields: name, description, status, url, tags
3. /projects updates automatically

### Update identity page
1. Edit `src/content/pages/index.mdx`
2. Push to main

### Publish a Forge session
1. Write session in `forge-sessions/YYYY-MM/YYYY-MM-DD-slug.md`
2. Copy to `src/content/writing/` with frontmatter
3. Push to main

### Git
- Content changes → push to main directly
- Feature changes → branch → merge when working

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| RESEND_API_KEY | Newsletter and contact form |

---

## Build Status

### Done
- [x] Domain on Cloudflare
- [x] Email routing to Gmail
- [x] Next.js + TypeScript + Tailwind scaffold
- [x] Design system live
- [x] Logo (Option B wordmark) and favicon
- [x] Avatar photo
- [x] Footer with socials
- [x] Nav with active states
- [x] MDX content system
- [x] projects.ts data file
- [x] Writing dynamic routing
- [x] Resend wired with API key
- [x] Contact API route

### In Progress
- [ ] Rebuild root page.tsx as Identity page
- [ ] Delete src/app/about/ and src/app/forge/
- [ ] Add The Forge to projects.ts
- [ ] Write real content for index.mdx
- [ ] First published article

### Up Next
- [ ] Newsletter signup to Resend audience list
- [ ] Reading time on article listings
- [ ] GEO explainer template
- [ ] First Agent Whitepaper

### Future
- [ ] forge.earnedconviction.com
- [ ] innerloop.earnedconviction.com
- [ ] zuari.earnedconviction.com
- [ ] warroom.earnedconviction.com
- [ ] Search across writing

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-14 | Initial PRD |
| 1.1 | 2026-03-14 | Simplified to four pages. Killed Home and About. Merged into Identity root. Moved Forge into Projects. |