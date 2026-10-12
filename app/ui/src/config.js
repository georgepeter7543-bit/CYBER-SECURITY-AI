/**
 * Global Frontend Configuration
 * Unified same-origin API endpoints with optional external override.
 * When VITE_BACKEND_URL is omitted, requests use relative endpoints (e.g. /api/...)
 * ensuring seamless same-origin communication with app/main.py.
 */

export const API_BASE_URL = (import.meta.env.VITE_BACKEND_URL || "").replace(/\/$/, "");

console.log(`[PETER SEC-OPS] API Gateway: ${API_BASE_URL ? API_BASE_URL : 'Same-Origin Relative (/api)'}`);
