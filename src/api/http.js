import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
export const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL ?? '/', headers: { Accept: 'application/json' } });
api.interceptors.request.use((config) => { const token = useAuthStore().accessToken; if (token)
    config.headers.Authorization = `Bearer ${token}`; return config; });
api.interceptors.response.use(r => r, async (error) => {
    const auth = useAuthStore();
    const original = error.config;
    if (error.response?.status === 401 && auth.refreshToken && !original._retry) {
        original._retry = true;
        await auth.refreshSession();
        original.headers.Authorization = `Bearer ${auth.accessToken}`;
        return api(original);
    }
    return Promise.reject(error);
});
//# sourceMappingURL=http.js.map