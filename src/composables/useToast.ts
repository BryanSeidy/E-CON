import { ref } from 'vue'

export type ToastType = 'success' | 'error' | 'info' | 'warning'

export interface Toast {
    id: string
    type: ToastType
    title: string
    message?: string
    duration?: number
}

const toasts = ref<Toast[]>([])

export function useToast() {
    function push(options: Omit<Toast, 'id'>) {
        const id = Math.random().toString(36).slice(2)
        const duration = options.duration ?? 4000
        toasts.value.push({ ...options, id })
        if (duration > 0) setTimeout(() => dismiss(id), duration)
    }

    function dismiss(id: string) {
        toasts.value = toasts.value.filter(t => t.id !== id)
    }

    const success = (title: string, message?: string) => push({ type: 'success', title, message })
    const error = (title: string, message?: string) => push({ type: 'error', title, message })
    const info = (title: string, message?: string) => push({ type: 'info', title, message })
    const warning = (title: string, message?: string) => push({ type: 'warning', title, message })

    return { toasts, push, dismiss, success, error, info, warning }
}