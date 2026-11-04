/** @type {import('next').NextConfig} */
const nextConfig = {
  // LOCAL ONLY: `npm run dev` proxies Python API; Vercel uses root vercel.json Services rewrites.
  async rewrites() { return process.env.NODE_ENV === 'development' ? [{ source: '/api/:path*', destination: 'http://127.0.0.1:8000/api/:path*' }] : []; },
};
export default nextConfig;