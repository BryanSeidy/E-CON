<script setup lang="ts">
import { CheckCircle2, AlertCircle, Info, AlertTriangle, X } from 'lucide-vue-next'
import { useToast } from '@/composables/useToast'

const { toasts, dismiss } = useToast()

const meta = {
  success: { icon: CheckCircle2, color: 'bg-emerald-50 border-emerald-200', text: 'text-emerald-900', icon_cls: 'text-emerald-500' },
  error:   { icon: AlertCircle,  color: 'bg-red-50 border-red-200',         text: 'text-red-900',     icon_cls: 'text-red-500'     },
  info:    { icon: Info,          color: 'bg-indigo-50 border-indigo-200',   text: 'text-indigo-900',  icon_cls: 'text-indigo-500'  },
  warning: { icon: AlertTriangle, color: 'bg-amber-50 border-amber-200',    text: 'text-amber-900',   icon_cls: 'text-amber-500'   },
} as const
</script>

<template>
  <Teleport to="body">
    <div class="fixed bottom-6 right-6 z-50 w-80 space-y-2">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="flex items-start gap-3 rounded-xl border p-4 shadow-lg"
          :class="[meta[toast.type].color, meta[toast.type].text]"
        >
          <component
            :is="meta[toast.type].icon"
            class="mt-0.5 h-4 w-4 shrink-0"
            :class="meta[toast.type].icon_cls"
          />
          <div class="min-w-0 flex-1">
            <p class="text-sm font-semibold">{{ toast.title }}</p>
            <p v-if="toast.message" class="mt-0.5 text-sm opacity-75">{{ toast.message }}</p>
          </div>
          <button
            class="shrink-0 opacity-50 transition-opacity hover:opacity-100"
            :aria-label="`Fermer la notification ${toast.title}`"
            @click="dismiss(toast.id)"
          >
            <X class="h-4 w-4" />
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active { transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1); }
.toast-enter-from,
.toast-leave-to     { opacity: 0; transform: translateX(0.75rem); }
.toast-move         { transition: transform 0.22s cubic-bezier(0.4, 0, 0.2, 1); }
</style>