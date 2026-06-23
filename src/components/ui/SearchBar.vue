<script setup lang="ts">
import { Search } from 'lucide-vue-next'

const model = defineModel<string>({ default: '' })
defineProps<{ placeholder?: string }>()
defineEmits<{ search: [value: string] }>()
</script>

<template>
  <label class="relative block w-full md:max-w-sm">
    <span class="sr-only">Rechercher</span>
    <Search class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
    <input
      v-model="model"
      type="search"
      class="w-full rounded-xl border border-border bg-white py-2.5 pl-10 pr-4 text-sm placeholder:text-slate-400 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-100"
      :placeholder="placeholder ?? 'Rechercher…'"
      @keyup.enter="$emit('search', model)"
    />
  </label>
</template>