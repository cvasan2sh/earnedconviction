# earnedconviction.com — Cowork Context

## What This Is
Personal brand and publishing platform for Siva Pentakota.
Built on The Forge — a multi-agent deliberation system.
Live at earnedconviction.com.

## The Person
Siva Pentakota. Transitioning from enterprise SaaS sales (Freshworks) to AI product building.
Strong abstract reasoning, high deliberation, cross-domain thinker.
North star: $100K ARR in B2B SaaS.

## Tech Stack
- Framework: Next.js App Router + TypeScript
- Styling: Tailwind CSS
- Hosting: Vercel free tier — auto-deploys on push to main
- DNS + Email: Cloudflare — siva@earnedconviction.com → Gmail
- Content: MDX files in src/content/
- Newsletter: Resend free tier
- Repo: github.com/cvasan2sh/earnedconviction
- Build tool: Cursor on Windows PC

## Design System — Never Violate
- Background: #1A1A1A
- Text: #F5F0E8
- Accent: #C0392B
- Display font: Playfair Display
- Body font: Source Serif 4
- No hero sections, no card grids, no purple gradients
- One animation per page maximum

## Site Structure — Four Pages Only
- / — Identity page (replaces Home + About)
- /writing — All articles and deliberations
- /projects — InnerLoop, Zuari, War-Room, The Forge
- /newsletter — Single signup

Nav: About (→ /), Writing, Projects, Newsletter

## Key File Locations
- Identity page: src/app/page.tsx
- Identity content: src/content/pages/index.mdx
- Articles: src/content/writing/YYYY-MM-DD-slug.mdx
- Projects data: src/data/projects.ts
- Forge sessions: forge-sessions/YYYY-MM/
- Components: src/app/components/
- MDX utilities: src/lib/mdx.ts

## Environment Variables
- RESEND_API_KEY — newsletter and contact form

## PRDs
- _cowork/PRD-site.md — website PRD
- _cowork/PRD-forge.md — The Forge system PRD

## Deployment
Push to main → Vercel auto-deploys → live in 60 seconds.