"use client";

import type { ReactNode } from "react";

type SocialKey = "linkedin" | "x" | "github";

export const SOCIAL_LINKS: Record<
  SocialKey,
  { label: string; href: string; icon: ReactNode }
> = {
  linkedin: {
    label: "LinkedIn",
    href: "https://www.linkedin.com/in/cvasan2sh",
    icon: (
      <svg
        viewBox="0 0 24 24"
        aria-hidden="true"
        className="h-4 w-4"
        fill="currentColor"
      >
        <path d="M20.45 20.45h-3.55v-5.56c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.95v5.65H9.36V9h3.41v1.56h.05c.47-.9 1.63-1.85 3.36-1.85 3.59 0 4.25 2.36 4.25 5.43v6.31ZM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12ZM7.12 20.45H3.56V9h3.56v11.45ZM22.23 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.46C23.2 24 24 23.23 24 22.28V1.72C24 .77 23.2 0 22.23 0Z" />
      </svg>
    ),
  },
  x: {
    label: "Twitter / X",
    href: "https://x.com/Siva_5kota",
    icon: (
      <svg
        viewBox="0 0 24 24"
        aria-hidden="true"
        className="h-4 w-4"
        fill="currentColor"
      >
        <path d="M18.9 2H22l-6.77 7.73L23.2 22h-6.6l-5.17-6.7L5.56 22H2.4l7.24-8.27L1 2h6.77l4.67 6.04L18.9 2Zm-1.16 18h1.72L6.62 3.9H4.78L17.74 20Z" />
      </svg>
    ),
  },
  github: {
    label: "GitHub",
    href: "https://github.com/cvasan2sh",
    icon: (
      <svg
        viewBox="0 0 24 24"
        aria-hidden="true"
        className="h-4 w-4"
        fill="currentColor"
      >
        <path d="M12 .5a12 12 0 0 0-3.79 23.39c.6.11.82-.26.82-.58v-2.07c-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.34-1.76-1.34-1.76-1.1-.75.08-.73.08-.73 1.21.09 1.85 1.24 1.85 1.24 1.08 1.84 2.83 1.31 3.52 1 .11-.78.42-1.31.76-1.61-2.66-.3-5.46-1.33-5.46-5.9 0-1.3.46-2.36 1.23-3.2-.12-.3-.54-1.52.12-3.17 0 0 1-.32 3.3 1.22a11.4 11.4 0 0 1 6 0c2.3-1.54 3.3-1.22 3.3-1.22.66 1.65.24 2.87.12 3.17.77.84 1.23 1.9 1.23 3.2 0 4.58-2.8 5.6-5.47 5.9.43.37.82 1.1.82 2.22v3.3c0 .32.22.69.82.58A12 12 0 0 0 12 .5Z" />
      </svg>
    ),
  },
};

