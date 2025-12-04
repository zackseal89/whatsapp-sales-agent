import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: true,
  // Use standard build for production (Turbopack is experimental)
  experimental: {
    // Turbopack only in dev mode
  },
};

export default nextConfig;
