/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  typedRoutes: true,
  turbopack: {
    root: __dirname
  },
  env: {
    NEXT_PUBLIC_DEFAULT_MODE: process.env.NEXT_PUBLIC_DEFAULT_MODE || "offline"
  }
};

module.exports = nextConfig;
