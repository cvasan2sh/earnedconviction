"use client";

import Link from "next/link";
import { SOCIAL_LINKS } from "./SocialIcons";

type Variant = "iconText" | "iconsOnly";

export default function SocialLinks({ variant }: { variant: Variant }) {
  const items = [SOCIAL_LINKS.linkedin, SOCIAL_LINKS.x, SOCIAL_LINKS.github];

  if (variant === "iconsOnly") {
    return (
      <div className="flex items-center justify-center gap-6">
        {items.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            target="_blank"
            rel="noopener noreferrer"
            aria-label={item.label}
            className="text-muted transition-colors hover:text-accent"
          >
            <span className="sr-only">{item.label}</span>
            {item.icon}
          </Link>
        ))}
      </div>
    );
  }

  return (
    <ul className="space-y-3">
      {items.map((item) => (
        <li key={item.href}>
          <Link
            href={item.href}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-3 font-body text-sm tracking-wide text-muted no-underline transition-colors hover:text-accent"
          >
            <span className="text-current">{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        </li>
      ))}
    </ul>
  );
}

