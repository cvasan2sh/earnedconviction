import type { Metadata } from "next";
import { Playfair_Display, Source_Serif_4 } from "next/font/google";
import "./globals.css";
import Nav from "./components/Nav";
import SocialLinks from "./components/SocialLinks";

const playfair = Playfair_Display({
  variable: "--font-playfair",
  subsets: ["latin"],
  display: "swap",
});

const sourceSerif = Source_Serif_4({
  variable: "--font-source-serif",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Earned Conviction | Siva Pentakota",
  description:
    "Personal brand and think tank — what I'm building, how I think, what I'm writing.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${playfair.variable} ${sourceSerif.variable}`}
    >
      <body className="min-h-screen antialiased">
        <Nav />
        <main className="animate-fade-in relative z-10 mx-auto max-w-[720px] px-6 pb-32 pt-16 lg:px-8">
          {children}
        </main>
        <footer className="relative z-10 border-t border-nav-border bg-background">
          <div className="mx-auto max-w-[720px] px-6 py-16 lg:px-8">
            <SocialLinks variant="iconsOnly" />
            <p className="mt-8 text-center font-body text-sm text-muted">
              © 2026 Siva Pentakota
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
