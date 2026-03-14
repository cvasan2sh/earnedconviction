"use client";

import { useState } from "react";

type Status = "idle" | "sending" | "sent" | "error";

export default function ContactForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState<Status>("idle");

  const buttonLabel =
    status === "sending"
      ? "Sending…"
      : status === "sent"
        ? "Sent"
        : status === "error"
          ? "Try again"
          : "Send";

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("sending");

    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, message }),
      });

      if (!res.ok) throw new Error("Failed to send");

      setStatus("sent");
      setName("");
      setEmail("");
      setMessage("");
    } catch {
      setStatus("error");
    }
  }

  const inputBase =
    "w-full rounded-sm border bg-transparent px-4 py-3 text-[#F5F0E8] placeholder:text-[#F5F0E8]/25 focus:border-[#C0392B] focus:outline-none";

  return (
    <form onSubmit={handleSubmit} className="max-w-lg space-y-6">
      <div>
        <label htmlFor="contact-name" className="mb-1.5 block text-sm text-[#F5F0E8]/60">
          Name
        </label>
        <input
          id="contact-name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          disabled={status === "sending"}
          className={`${inputBase} border-[#F5F0E8]/15`}
          placeholder="Your name"
        />
      </div>
      <div>
        <label htmlFor="contact-email" className="mb-1.5 block text-sm text-[#F5F0E8]/60">
          Email
        </label>
        <input
          id="contact-email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          disabled={status === "sending"}
          className={`${inputBase} border-[#F5F0E8]/15`}
          placeholder="you@example.com"
        />
      </div>
      <div>
        <label htmlFor="contact-message" className="mb-1.5 block text-sm text-[#F5F0E8]/60">
          Message
        </label>
        <textarea
          id="contact-message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          required
          disabled={status === "sending"}
          rows={5}
          className={`${inputBase} resize-none border-[#F5F0E8]/15`}
          placeholder="Your message"
        />
      </div>
      <button
        type="submit"
        disabled={status === "sending"}
        className="rounded-sm border border-[#F5F0E8]/20 bg-transparent px-6 py-3 text-[#F5F0E8] transition-colors hover:border-[#C0392B] disabled:opacity-50"
      >
        {buttonLabel}
      </button>
    </form>
  );
}
