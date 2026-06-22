import { defineStore } from 'pinia'
import type { UnwrapRef } from 'vue'
import type { ListParams } from '@/api/resource'

export function createResourceStore<TList>(id: string, listFn: (params?: ListParams) => Promise<TList>) {
  return defineStore(id, {
    state: () => ({
      data: null as TList | null,
      loading: false,
      error: null as string | null,
      params: {} as ListParams,
    }),
    actions: {
      async fetch(params?: ListParams) {
        this.loading = true
        this.error = null
        this.params = { ...this.params, ...params }
        try {
          this.$patch({ data: (await listFn(this.params)) as TList })
        } catch (e) {
          this.error = e instanceof Error ? e.message : 'Erreur de chargement'
        } finally {
          this.loading = false
        }
      },
    },
  })
  return defineStore(id, { state: () => ({ data: null as TList | null, loading: false, error: null as string | null, params: {} as ListParams }), actions: { async fetch(params?: ListParams) { this.loading = true; this.error = null; this.params = { ...this.params, ...params }; try { this.data = await listFn(this.params) as UnwrapRef<TList> } catch (e) { this.error = e instanceof Error ? e.message : 'Erreur de chargement' } finally { this.loading = false } } } })
}
