"use client";

import { useState } from "react";

type Status = "idle" | "sending" | "sent" | "error";

export default function NewsletterForm() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<Status>("idle");

  const buttonLabel =
    status === "sending"
      ? "Subscribing…"
      : status === "sent"
        ? "Subscribed"
        : status === "error"
          ? "Try again"
          : "Subscribe";

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("sending");

    try {
      const res = await fetch("/api/newsletter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      if (!res.ok) throw new Error("Failed to subscribe");

      setStatus("sent");
      setEmail("");
    } catch {
      setStatus("error");
    }
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-lg space-y-6">
      <div>
        <label htmlFor="newsletter-email" className="mb-1.5 block text-sm text-[#F5F0E8]/60">
          Email
        </label>
        <input
          id="newsletter-email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          disabled={status === "sending"}
          className="w-full rounded-sm border border-[#F5F0E8]/15 bg-transparent px-4 py-3 text-[#F5F0E8] placeholder:text-[#F5F0E8]/25 focus:border-[#C0392B] focus:outline-none"
          placeholder="you@example.com"
        />
      </div>
      <button
        type="submit"
        disabled={status === "sending" || status === "sent"}
        className="rounded-sm border border-[#F5F0E8]/20 bg-transparent px-6 py-3 text-[#F5F0E8] transition-colors hover:border-[#C0392B] disabled:opacity-50"
      >
        {buttonLabel}
      </button>
      {status === "sent" && (
        <p className="text-sm text-[#F5F0E8]/60">
          You&apos;re in. I&apos;ll be in touch.
        </p>
      )}
    </form>
  );
}
