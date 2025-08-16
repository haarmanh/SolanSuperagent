import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Vercel deployment optimizations
  experimental: {
    serverComponentsExternalPackages: [],
  },

  // Security headers for production
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data: https:;",
          },
        ],
      },
    ];
  },

  // Environment variables
  env: {
    CUSTOM_ENV: process.env.NODE_ENV || 'production',
  },
};

export default nextConfig;
