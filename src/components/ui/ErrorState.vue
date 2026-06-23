<script setup lang="ts">
import { AlertCircle, RefreshCw } from 'lucide-vue-next'

defineProps<{
  message?: string
}>()

defineEmits<{ retry: [] }>()
</script>

<template>
  <div class="flex items-start gap-4 rounded-2xl border border-red-200 bg-red-50 p-6">
    <AlertCircle class="mt-0.5 h-5 w-5 shrink-0 text-red-500" />
    <div class="flex-1">
      <p class="text-sm font-semibold text-red-800">Une erreur est survenue</p>
      <p v-if="message" class="mt-1 text-sm text-red-700">{{ message }}</p>
    </div>
    <button
      v-if="$attrs.onRetry"
      class="flex items-center gap-1.5 rounded-xl border border-red-200 bg-white px-3 py-1.5 text-xs font-medium text-red-700 transition-colors hover:bg-red-50"
      @click="$emit('retry')"
    >
      <RefreshCw class="h-3 w-3" /> Réessayer
    </button>
  </div>
</template>