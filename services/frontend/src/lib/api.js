import { API_BASE } from "../config/env";

async function httpJson(url, opts) {
  const res = await fetch(url, opts);
  if (!res.ok) {
    let text = await res.text().catch(() => "");
    if (text && text.length > 400) text = text.slice(0, 400) + "…";
    throw new Error(`${opts?.method || "GET"} ${url} failed: ${res.status} ${text}`);
  }

  const ct = res.headers.get("content-type") || "";
  if (!ct.includes("application/json")) {
    const text = await res.text().catch(() => "");
    throw new Error(`Expected JSON from ${url} but got: ${ct || "unknown"} ${text.slice(0, 200)}`);
  }
  return res.json();
}

function join(base, path) {
  const b = (base || "").replace(/\/+$/, "");
  const p = (path || "").replace(/^\/+/, "");
  if (!b) return `/${p}`;
  return `${b}/${p}`;
}

function apiUrl(path, params) {
  const urlStr = join(API_BASE, path);


  const url = API_BASE.startsWith("http")
    ? new URL(urlStr)
    : new URL(urlStr, window.location.href);

  if (params) {
    for (const [k, v] of Object.entries(params)) {
      if (v !== null && v !== undefined && v !== "") url.searchParams.set(k, String(v));
    }
  }
  return url.toString();
}

export function getSamples({ limit = 200, offset = 0, from_time = null, to_time = null } = {}) {
  return httpJson(apiUrl("samples", { limit, offset, from_time, to_time }));
}

export function ingestSamples(payload) {
  return httpJson(apiUrl("samples"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function filterSamples({ polygon, from_time = null, to_time = null, limit = 5000, offset = 0 }) {
  return httpJson(apiUrl("samples/filter"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ polygon, from_time, to_time, limit, offset }),
  });
}
