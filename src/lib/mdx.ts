import fs from "fs/promises";
import matter from "gray-matter";
import path from "path";

const PAGES_DIR = path.join(process.cwd(), "src", "content", "pages");
const WRITING_DIR = path.join(process.cwd(), "src", "content", "writing");

export type WritingPostMeta = {
  slug: string;
  title: string;
  date: string;
  description: string;
  tags: string[];
  stage?: string;
  agents?: string[];
};

export async function getPageContent(slug: string) {
  const filePath = path.join(PAGES_DIR, `${slug}.mdx`);
  const raw = await fs.readFile(filePath, "utf-8");
  const { data: frontmatter, content } = matter(raw);
  return { frontmatter, content };
}

export async function getAllWritingPosts(): Promise<WritingPostMeta[]> {
  const files = await fs.readdir(WRITING_DIR);
  const mdxFiles = files.filter((f) => f.endsWith(".mdx"));

  const posts = await Promise.all(
    mdxFiles.map(async (file) => {
      const slug = file.replace(/\.mdx$/, "");
      const filePath = path.join(WRITING_DIR, file);
      const raw = await fs.readFile(filePath, "utf-8");
      const { data } = matter(raw);
      return {
        slug,
        title: data.title ?? slug,
        date: data.date ?? "",
        description: data.description ?? "",
        tags: Array.isArray(data.tags) ? data.tags : [],
        stage: data.stage,
        agents: Array.isArray(data.agents) ? data.agents : [],
      };
    })
  );

  return posts.sort((a, b) => (b.date > a.date ? 1 : -1));
}

export async function getWritingPost(slug: string) {
  const filePath = path.join(WRITING_DIR, `${slug}.mdx`);
  const raw = await fs.readFile(filePath, "utf-8");
  const { data: frontmatter, content } = matter(raw);
  return { frontmatter, content };
}
