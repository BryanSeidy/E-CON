<script setup lang="ts">
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'

const props = defineProps<{
  page: number
  total: number
  pageSize?: number
}>()

const emit = defineEmits<{ 'update:page': [page: number] }>()

const pageSize = props.pageSize ?? 20
const totalPages = Math.max(1, Math.ceil(props.total / pageSize))

const prev = () => emit('update:page', props.page - 1)
const next = () => emit('update:page', props.page + 1)
</script>

<template>
  <div
    v-if="total > pageSize"
    class="flex items-center justify-between rounded-2xl border border-border bg-white p-4"
  >
    <button
      class="flex items-center gap-1.5 rounded-xl border border-border px-3 py-2 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
      :disabled="page <= 1"
      @click="prev"
    >
      <ChevronLeft class="h-4 w-4" /> Précédent
    </button>
    <span class="text-sm text-slate-500">Page {{ page }} sur {{ totalPages }}</span>
    <button
      class="flex items-center gap-1.5 rounded-xl border border-border px-3 py-2 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
      :disabled="page >= totalPages"
      @click="next"
    >
      Suivant <ChevronRight class="h-4 w-4" />
    </button>
  </div>
</template>