"use client";

import Image from "next/image";
import { useState } from "react";

export default function Avatar({
  size = 160,
  initials = "SP",
}: {
  size?: number;
  initials?: string;
}) {
  const [failed, setFailed] = useState(false);

  if (failed) {
    return (
      <div
        aria-label="Avatar placeholder"
        className="flex items-center justify-center rounded-full font-display text-accent"
        style={{
          width: size,
          height: size,
          backgroundColor: "#2A2A2A",
        }}
      >
        <span className="text-2xl tracking-tight">{initials}</span>
      </div>
    );
  }

  return (
    <Image
      src="/avatar.jpg"
      alt="Siva Pentakota"
      width={size}
      height={size}
      className="rounded-full"
      onError={() => setFailed(true)}
      priority
    />
  );
}

