import { api } from './http'
export interface ListParams { page?: number; search?: string; ordering?: string; [key: string]: unknown }
export const resourceClient = <TList, TDetail, TCreate = Partial<TDetail>, TUpdate = Partial<TCreate>>(base: string) => ({
  list: (params?: ListParams) => api.get<TList>(base, { params }).then(r => r.data),
  retrieve: (id: string) => api.get<TDetail>(`${base}${id}/`).then(r => r.data),
  create: (payload: TCreate | FormData) => api.post<TDetail>(base, payload).then(r => r.data),
  update: (id: string, payload: TUpdate | FormData) => api.patch<TDetail>(`${base}${id}/`, payload).then(r => r.data),
  remove: (id: string) => api.delete(`${base}${id}/`).then(r => r.data),
  action: <TResponse = TDetail>(id: string, action: string, payload?: unknown) => api.post<TResponse>(`${base}${id}/${action}/`, payload).then(r => r.data),
})
