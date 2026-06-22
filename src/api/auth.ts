import { api } from './http'
import type { TokenObtainPair, TokenObtainPairRequest, TokenRefresh } from '@/types/api'
export const authApi = { login: (payload: TokenObtainPairRequest) => api.post<TokenObtainPair>('/api/v1/auth/token/', payload).then(r=>r.data), refresh: (refresh: string) => api.post<TokenRefresh>('/api/v1/auth/token/refresh/', { refresh }).then(r=>r.data) }
