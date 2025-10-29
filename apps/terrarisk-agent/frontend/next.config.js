/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    typedRoutes: true
  },
  env: {
    NEXT_PUBLIC_DEFAULT_MODE: process.env.NEXT_PUBLIC_DEFAULT_MODE || "offline"
  }
};

module.exports = nextConfig;
