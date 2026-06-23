<script setup lang="ts">
const props = defineProps<{ status: string }>()

const MAP: Record<string, string> = {
  // Application
  PENDING:      'bg-amber-50  text-amber-700  border-amber-200',
  REVIEWED:     'bg-blue-50   text-blue-700   border-blue-200',
  ACCEPTED:     'bg-emerald-50 text-emerald-700 border-emerald-200',
  REJECTED:     'bg-red-50    text-red-700    border-red-200',
  // Internship
  ASSIGNED:     'bg-slate-100 text-slate-700  border-slate-200',
  ACTIVE:       'bg-indigo-50 text-indigo-700 border-indigo-200',
  COMPLETED:    'bg-emerald-50 text-emerald-700 border-emerald-200',
  CANCELLED:    'bg-red-50    text-red-700    border-red-200',
  // Document
  UPLOADED:     'bg-blue-50   text-blue-700   border-blue-200',
  IN_REVIEW:    'bg-violet-50 text-violet-700 border-violet-200',
  APPROVED:     'bg-emerald-50 text-emerald-700 border-emerald-200',
}

const LABELS: Record<string, string> = {
  PENDING:   'En attente',
  REVIEWED:  'Examinée',
  ACCEPTED:  'Acceptée',
  REJECTED:  'Rejetée',
  ASSIGNED:  'Assigné',
  ACTIVE:    'Actif',
  COMPLETED: 'Terminé',
  CANCELLED: 'Annulé',
  UPLOADED:  'Déposé',
  IN_REVIEW: 'En revue',
  APPROVED:  'Approuvé',
}

const cls = MAP[props.status]  ?? 'bg-slate-100 text-slate-600 border-slate-200'
const label = LABELS[props.status] ?? props.status
</script>

<template>
  <span
    class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium"
    :class="cls"
  >{{ label }}</span>
</template>