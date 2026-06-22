import { defineStore } from 'pinia'
import { z } from 'zod'
import { authApi } from '@/api/auth'
import type { SessionUser, UserRole } from '@/types/auth'
const loginSchema = z.object({ email: z.string().email(), password: z.string().min(1) })
const roles = ['STUDENT','COMPANY_MEMBER','ACADEMIC_SUPERVISOR','HEAD_OF_PROGRAM','UNIVERSITY_ADMIN','SUPER_ADMIN'] as const
function decodeJwt(token: string): Record<string, unknown> { try { return JSON.parse(atob(token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/'))) } catch { return {} } }
function userFromToken(token: string): SessionUser { const p = decodeJwt(token); const role = roles.includes(p.role as UserRole) ? p.role as UserRole : undefined; return { id: String(p.user_id ?? p.sub ?? ''), email: typeof p.email === 'string' ? p.email : undefined, role } }
export const useAuthStore = defineStore('auth', {
  state: () => ({ accessToken: localStorage.getItem('econ.access'), refreshToken: localStorage.getItem('econ.refresh'), user: JSON.parse(localStorage.getItem('econ.user') || 'null') as SessionUser | null, initialized: false }),
  getters: { isAuthenticated: s => Boolean(s.accessToken), role: s => s.user?.role },
  actions: {
    async login(input: unknown) { const credentials = loginSchema.parse(input); const tokens = await authApi.login(credentials); this.setSession(tokens.access, tokens.refresh) },
    setSession(access: string, refresh: string) { this.accessToken = access; this.refreshToken = refresh; this.user = userFromToken(access); localStorage.setItem('econ.access', access); localStorage.setItem('econ.refresh', refresh); localStorage.setItem('econ.user', JSON.stringify(this.user)) },
    async refreshSession() { if (!this.refreshToken) throw new Error('Missing refresh token'); const tokens = await authApi.refresh(this.refreshToken); this.setSession(tokens.access, tokens.refresh) },
    logout() { this.accessToken = null; this.refreshToken = null; this.user = null; localStorage.removeItem('econ.access'); localStorage.removeItem('econ.refresh'); localStorage.removeItem('econ.user') },
  },
})
