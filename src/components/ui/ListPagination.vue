<script setup lang="ts">
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'

defineProps<{
  page: number
  totalPages: number
  total: number
  pageSize?: number
}>()

const emit = defineEmits<{
  previous: []
  next: []
}>()
</script>

<template>
  <div
    v-if="total > (pageSize ?? 20)"
    class="flex items-center justify-between rounded-2xl border border-border bg-white p-4"
  >
    <button
      class="rounded-xl border border-border px-3 py-2 text-sm disabled:opacity-50"
      :disabled="page === 1"
      @click="emit('previous')"
    >
      <ChevronLeft class="mr-1 inline h-4 w-4" />
      Précédent
    </button>
    <span class="text-sm text-slate-500">
      Page {{ page }} sur {{ totalPages }} · {{ total }} résultat{{ total > 1 ? 's' : '' }}
    </span>
    <button
      class="rounded-xl border border-border px-3 py-2 text-sm disabled:opacity-50"
      :disabled="page === totalPages"
      @click="emit('next')"
    >
      Suivant
      <ChevronRight class="ml-1 inline h-4 w-4" />
    </button>
  </div>
</template>
