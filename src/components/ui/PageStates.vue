<script setup lang="ts">
defineProps<{
  loading?: boolean
  error?: string
  empty?: boolean
  emptyMessage?: string
  skeletonCount?: number
}>()
</script>

<template>
  <div v-if="loading" class="grid gap-4 md:grid-cols-2">
    <div
      v-for="i in skeletonCount ?? 4"
      :key="i"
      class="h-40 animate-pulse rounded-2xl bg-slate-200"
    />
  </div>
  <div
    v-else-if="error"
    class="rounded-2xl border border-red-200 bg-red-50 p-6 text-red-700"
  >
    {{ error }}
  </div>
  <div
    v-else-if="empty"
    class="rounded-2xl border border-border bg-white p-10 text-center text-slate-500"
  >
    {{ emptyMessage ?? 'Aucun élément trouvé.' }}
  </div>
  <slot v-else />
</template>
