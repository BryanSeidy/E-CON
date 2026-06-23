<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { dashboardApi } from '@/api/endpoints';
import { useAuthStore } from '@/stores/auth';
import type { DashboardSummary } from '@/types/api';
import PageHeader from '@/components/ui/PageHeader.vue';
import BaseCard from '@/components/ui/BaseCard.vue';
import ErrorState from '@/components/ui/ErrorState.vue';

const auth = useAuthStore();
const data = ref<DashboardSummary | null>(null);
const loading = ref(true);
const error = ref("");

const LABEL_MAP: Record<string, string> = {
  applications:          'Candidatures',
  pending_applications:  'En attente',
  active_offers:         'Offres actives',
  assigned_internships:  'Stages assignés',
  active_internships:    'Stages actifs',
  completed_internships: 'Stages terminés',
  documents:             'Documents',
  documents_to_review:   'Docs à réviser',
  rejected_documents:    'Docs rejetés',
  weekly_logs:           'Journaux hebdo',
  unread_notifications:  'Non lus',
}

/* highlight a metric to draw the eye */
const ACCENT: Record<string, string> = {
  active_internships:   'border-l-4 border-l-indigo-500',
  pending_applications: 'border-l-4 border-l-amber-400',
  unread_notifications: 'border-l-4 border-l-rose-400',
}

const loader = computed(() =>
  auth.role === 'COMPANY_MEMBER'
    ? dashboardApi.company
    : ['UNIVERSITY_ADMIN','ACADEMIC_SUPERVISOR','HEAD_OF_PROGRAM'].includes(auth.role ?? '')
      ? dashboardApi.university
      : dashboardApi.student,
);

async function load() {
  loading.value = true
  error.value   = ''
  try {
    data.value = await loader.value()
  } catch {
    error.value = 'Impossible de charger le tableau de bord.'
  } finally {
    loading.value = false
  }
}

onMounted(load)

const cards = computed(() =>
  Object.entries(data.value ?? {})
    .filter(([, v]) => v !== undefined)
    .map(([k, v]) => ({ key: k, label: LABEL_MAP[k] ?? k.replaceAll('_', ' '), value: v as number }))
)
</script>

<template>
  <div class="space-y-6">
    <PageHeader
      eyebrow="Vue d'ensemble"
      title="Tableau de bord"
      description="Indicateurs retournés par le backend selon votre rôle."
    />

    <!-- Skeleton -->
    <div v-if="loading" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3" aria-busy="true">
      <div
        v-for="i in 6"
        :key="i"
        class="h-28 animate-pulse rounded-2xl bg-slate-100"
        aria-hidden="true"
      />
    </div>
    
    <!-- Error -->
    <ErrorState v-else-if="error" :message="error" @retry="load" />

    <!-- Empty -->
    <BaseCard v-else-if="!cards.length" class="py-16 text-center">
      <p class="text-sm text-slate-400">Aucune donnée disponible pour ce rôle.</p>
    </BaseCard>

    <!-- Grid -->
    <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <article
        v-for="card in cards"
        :key="card.key"
        class="rounded-2xl border border-border bg-white p-6 shadow-sm transition-shadow hover:shadow-md"
        :class="ACCENT[card.key] ?? ''"
      >
        <p class="text-xs font-semibold uppercase tracking-widest text-slate-400">{{ card.label }}</p>
        <p class="mt-3 text-4xl font-bold tabular-nums tracking-tight text-slate-900">
          {{ card.value?.toLocaleString('fr-FR') ?? '—' }}
        </p>
      </article>
    </div>
  </div>
</template>