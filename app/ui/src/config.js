/**
 * Global Frontend Configuration
 * Dynamic backend resolution supporting Vercel production deployment
 * paired with Render, Railway, or local development environments.
 */

export const API_BASE_URL = (
  import.meta.env.VITE_BACKEND_URL || "http://localhost:5000"
).replace(/\/$/, "");

console.log(`[PETER SEC-OPS] Active Backend Gateway: ${API_BASE_URL}`);
