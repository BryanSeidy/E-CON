import { defineStore } from 'pinia';
export function createResourceStore(id, listFn) {
    return defineStore(id, {
        state: () => ({
            data: null,
            loading: false,
            error: null,
            params: {},
        }),
        actions: {
            async fetch(params) {
                this.loading = true;
                this.error = null;
                this.params = { ...this.params, ...params };
                try {
                    this.$patch({ data: (await listFn(this.params)) });
                }
                catch (e) {
                    this.error = e instanceof Error ? e.message : 'Erreur de chargement';
                }
                finally {
                    this.loading = false;
                }
            },
        },
    });
}
//# sourceMappingURL=resources.js.map