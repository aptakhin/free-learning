/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  eslint: {
    // Warning: This allows production builds to successfully complete even if
    // your project has ESLint errors.
    ignoreDuringBuilds: true,
  },
  typescript: {
    // !! WARN !!
    // Dangerously allow production builds to successfully complete even if
    // your project has type errors.
    // !! WARN !!
    ignoreBuildErrors: true,
  },
  images: { unoptimized: true },
  trailingSlash: true,
//   exportPathMap: async function (
//     defaultPathMap,
//     { dev, dir, outDir, distDir, buildId }
//   ) {
//     return {
//       '/': { page: '/' },
//       // '/about': { page: '/about' },
//       // '/p/hello-nextjs': { page: '/post', query: { title: 'hello-nextjs' } },
//       // '/p/learn-nextjs': { page: '/post', query: { title: 'learn-nextjs' } },
//       // '/p/deploy-nextjs': { page: '/post', query: { title: 'deploy-nextjs' } },
//     }
//   },
}

module.exports = nextConfig
