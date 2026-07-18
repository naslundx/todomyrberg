export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  const res = await fetch(`/api${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });
  if (!res.ok) {
    throw new Error(`API Error: ${res.statusText}`);
  }
  if (res.status === 204) {
    return null;
  }
  return res.json();
}
