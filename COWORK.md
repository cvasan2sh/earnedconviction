# earnedconviction.com — Cowork Context File

## What this project is
Personal brand, think tank, and publishing platform for Siva Pentakota.
Built on The Forge — a multi-agent deliberation system.
Live at earnedconviction.com.

## Tech stack
Next.js App Router, TypeScript, Tailwind CSS, Vercel, Cloudflare, Resend

## Conventions

### Adding a new article
1. Create a new .mdx file in src/content/writing/
2. Filename format: YYYY-MM-DD-slug.mdx
3. Required frontmatter:
   - title
   - date (YYYY-MM-DD)
   - description (one sentence)
   - tags (array)
   - stage (0-1 / 1-10 / 10-100)
   - agents (array of agent names active in session)
4. Push to main — Vercel auto-deploys

### Adding a new project
1. Open src/data/projects.ts
2. Add entry to the projects array
3. Fields: name, description, status, url, tags
4. Both homepage and /projects page update automatically

### Updating static page content
1. Edit the relevant .mdx file in src/content/pages/
2. forge.mdx → The Forge page
3. about.mdx → About page
4. Push to main

### Saving a Forge session
1. Create new file in forge-sessions/YYYY-MM/
2. Filename format: YYYY-MM-DD-problem-slug.md
3. Use _template.md as the starting structure
4. If publishing — copy to src/content/writing/ with correct frontmatter

### Design rules — never violate
- Background: #1A1A1A
- Text: #F5F0E8
- Accent: #C0392B
- Fonts: Playfair Display (display), Source Serif 4 (body)
- No hero sections, no card grids, no purple gradients

## Deployment
Push to main branch → Vercel auto-deploys → live within 60 seconds