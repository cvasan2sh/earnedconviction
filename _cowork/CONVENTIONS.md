# Conventions

## Adding a new article
1. Create file: src/content/writing/YYYY-MM-DD-slug.mdx
2. Required frontmatter:
   - title: string
   - date: YYYY-MM-DD
   - description: one sentence
   - tags: [array]
   - stage: 0-1 | 1-10 | 10-100
   - agents: [array of agent names]
3. Push to main → Vercel auto-deploys

## Adding a new project
1. Open src/data/projects.ts
2. Add to projects array
3. Fields: name, description, status, url, tags
4. Homepage and /projects update automatically

## Updating page content
1. Edit src/content/pages/[page].mdx
2. forge.mdx → The Forge page
3. about.mdx → About page
4. Push to main

## Saving a Forge session
1. Create file in forge-sessions/YYYY-MM/
2. Use _template.md as structure
3. If publishing → copy to src/content/writing/ with frontmatter

## Git workflow
- Small changes → commit + push to main directly
- New features → new branch → merge when working
- Every push to main → Vercel auto-deploys in 60 seconds