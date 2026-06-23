<script setup lang="ts">
defineProps<{
  eyebrow?: string
  title: string
  description?: string
}>()
</script>

<template>
  <div class="rounded-2xl border border-border bg-white p-6 shadow-sm">
    <p v-if="eyebrow" class="text-xs font-semibold uppercase tracking-widest text-slate-400">{{ eyebrow }}</p>
    <h2 class="mt-1 text-2xl font-bold tracking-tight text-slate-900">{{ title }}</h2>
    <p v-if="description" class="mt-2 max-w-2xl text-sm text-slate-500">{{ description }}</p>
    <slot />
  </div>
</template>