/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // Environment variables
  env: {
    NEXT_PUBLIC_API_BASE: process.env.NEXT_PUBLIC_API_BASE || 'https://api.solanai.ai',
    NEXT_PUBLIC_SITE_URL: process.env.NEXT_PUBLIC_SITE_URL || 'https://solanai.ai',
  },

  // Security headers
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
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com; style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; img-src 'self' data: https:; connect-src 'self' https://api.solanai.ai;",
          },
        ],
      },
    ];
  },

  // Redirects
  async redirects() {
    return [
      {
        source: '/observatorium',
        destination: '/dashboard',
        permanent: false,
      },
    ];
  },

  // API rewrites for development
  async rewrites() {
    return [
      {
        source: '/api/proxy/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_BASE}/api/:path*`,
      },
    ];
  },

  // Image optimization
  images: {
    domains: ['solanai.ai'],
    formats: ['image/webp', 'image/avif'],
  },

  // Compression
  compress: true,

  // Performance optimizations
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['lucide-react', 'recharts'],
  },
};

module.exports = nextConfig;
