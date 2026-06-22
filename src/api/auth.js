import { api } from './http';
export const authApi = { login: (payload) => api.post('/api/v1/auth/token/', payload).then(r => r.data), refresh: (refresh) => api.post('/api/v1/auth/token/refresh/', { refresh }).then(r => r.data) };
//# sourceMappingURL=auth.js.map