"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const links = [
  { href: "/", label: "Home" },
  { href: "/about", label: "About" },
  { href: "/forge", label: "The Forge" },
  { href: "/writing", label: "Writing" },
  { href: "/projects", label: "Projects" },
  { href: "/newsletter", label: "Newsletter" },
];

export default function Nav() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header
      className="sticky top-0 z-20 border-b border-nav-border bg-background/95 backdrop-blur-sm"
      style={{ backgroundColor: "rgba(26, 26, 26, 0.95)" }}
    >
      <nav className="mx-auto flex max-w-[720px] items-center justify-between gap-8 px-6 py-5 lg:px-8">
        <Link href="/" className="no-underline">
          <Image
            src="/logo.svg"
            alt="Earned Conviction"
            height={36}
            width={117}
            className="h-9 w-auto"
            priority
          />
        </Link>

        <ul className="hidden items-center gap-8 sm:flex">
          {links.map((link) => (
            <li key={link.href}>
              <Link
                href={link.href}
                className={`font-body text-sm uppercase tracking-wide no-underline transition-colors hover:text-accent ${
                  pathname === link.href ? "text-accent" : "text-foreground/80"
                }`}
              >
                {link.label}
              </Link>
            </li>
          ))}
        </ul>

        <button
          type="button"
          className="flex flex-col gap-1.5 sm:hidden"
          onClick={() => setMobileOpen((o) => !o)}
          aria-expanded={mobileOpen}
          aria-label="Toggle menu"
        >
          <span
            className={`h-0.5 w-5 bg-foreground transition ${mobileOpen ? "translate-y-2 rotate-45" : ""}`}
          />
          <span
            className={`h-0.5 w-5 bg-foreground transition ${mobileOpen ? "opacity-0" : ""}`}
          />
          <span
            className={`h-0.5 w-5 bg-foreground transition ${mobileOpen ? "-translate-y-2 -rotate-45" : ""}`}
          />
        </button>
      </nav>

      {mobileOpen && (
        <ul className="flex flex-col gap-4 border-t border-nav-border px-6 py-5 sm:hidden">
          {links.map((link) => (
            <li key={link.href}>
              <Link
                href={link.href}
                className={`block font-body text-sm uppercase tracking-wide no-underline transition-colors hover:text-accent ${
                  pathname === link.href ? "text-accent" : "text-foreground/80"
                }`}
                onClick={() => setMobileOpen(false)}
              >
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      )}
    </header>
  );
}
