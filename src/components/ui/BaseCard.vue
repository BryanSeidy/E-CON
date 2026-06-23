<script setup lang="ts">
defineProps<{
  padding?: 'none' | 'sm' | 'md' | 'lg'
  shadow?: boolean
  border?: boolean
}>()
</script>

<template>
  <div
    class="rounded-2xl bg-white"
    :class="{
      'border border-border': border !== false,
      'shadow-sm': shadow !== false,
      'p-0':  padding === 'none',
      'p-4':  padding === 'sm',
      'p-6':  padding === undefined || padding === 'md',
      'p-8':  padding === 'lg',
    }"
  >
    <slot />
  </div>
</template>