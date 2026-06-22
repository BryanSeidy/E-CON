import { api } from './http';
export const resourceClient = (base) => ({
    list: (params) => api.get(base, { params }).then(r => r.data),
    retrieve: (id) => api.get(`${base}${id}/`).then(r => r.data),
    create: (payload) => api.post(base, payload).then(r => r.data),
    update: (id, payload) => api.patch(`${base}${id}/`, payload).then(r => r.data),
    remove: (id) => api.delete(`${base}${id}/`).then(r => r.data),
    action: (id, action, payload) => api.post(`${base}${id}/${action}/`, payload).then(r => r.data),
});
//# sourceMappingURL=resource.js.map