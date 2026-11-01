const BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${BASE}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...(init.headers || {}) },
  })
  if (!response.ok) {
    let message = `Request failed (${response.status})`
    try { const body = await response.json(); message = body.detail || message } catch {}
    throw new Error(typeof message === 'string' ? message : JSON.stringify(message))
  }
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}
export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body: unknown) => request<T>(path, { method: 'POST', body: JSON.stringify(body) }),
  put: <T>(path: string, body: unknown) => request<T>(path, { method: 'PUT', body: JSON.stringify(body) }),
  delete: (path: string) => request<void>(path, { method: 'DELETE' }),
}
