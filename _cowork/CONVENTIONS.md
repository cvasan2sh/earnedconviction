# earnedconviction.com — Conventions

## Adding a New Article
1. Create: `src/content/writing/YYYY-MM-DD-slug.mdx`
2. Required frontmatter:
```yaml
---
title:
date: YYYY-MM-DD
description: One sentence summary
tags: []
stage: 0-1 | 1-10 | 10-100
agents: []
---
```
3. Push to main → live in 60 seconds

## Adding a New Project
1. Open `src/data/projects.ts`
2. Add entry to projects array
3. Fields: name, description, status, url, tags
4. /projects page updates automatically — no other changes needed

## Updating the Identity Page
1. Edit `src/content/pages/index.mdx`
2. Push to main

## Publishing a Forge Session
1. Write session in `forge-sessions/YYYY-MM/YYYY-MM-DD-slug.md`
2. Use `forge-sessions/_template.md` as structure
3. When ready → copy to `src/content/writing/` with correct frontmatter
4. Push to main

## Git Workflow
- Content changes, small fixes → commit + push to main directly
- New features, layout changes → new branch → merge when working
- Commit messages in plain English — describe what changed

## Naming Conventions
- Article files: YYYY-MM-DD-descriptive-slug.mdx
- Forge session files: YYYY-MM-DD-problem-slug.md
- Components: PascalCase.tsx
- Utilities: camelCase.ts

## What NOT to Do
- Never hardcode content in .tsx page files — use MDX files
- Never add projects directly to page components — use projects.ts only
- Never commit .env.local — it is gitignored via .env*
- Never violate the design system — see CONTEXT.md
- Never create new top-level pages without updating PRD-site.md first