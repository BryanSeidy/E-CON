<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { dashboardApi } from "@/api/endpoints";
import { useAuthStore } from "@/stores/auth";
import type { DashboardSummary } from "@/types/api";
const auth = useAuthStore();
const data = ref<DashboardSummary | null>(null);
const loading = ref(true);
const error = ref("");
const loader = computed(() =>
  auth.role === "COMPANY_MEMBER"
    ? dashboardApi.company
    : ["UNIVERSITY_ADMIN", "ACADEMIC_SUPERVISOR", "HEAD_OF_PROGRAM"].includes(
          auth.role ?? "",
        )
      ? dashboardApi.university
      : dashboardApi.student,
);
onMounted(async () => {
  try {
    data.value = await loader.value();
  } catch {
    error.value = "Impossible de charger le dashboard.";
  } finally {
    loading.value = false;
  }
});
const cards = computed(() =>
  Object.entries(data.value ?? {}).map(([k, v]) => ({
    label: k.replaceAll("_", " "),
    value: v,
  })),
);
</script>
<template>
  <div class="space-y-6">
    <div class="rounded-2xl border border-border bg-white p-6">
      <h2 class="text-2xl font-semibold">Vue d’ensemble</h2>
      <p class="mt-2 text-slate-500">
        Indicateurs retournés par le backend selon votre rôle.
      </p>
    </div>
    <div v-if="loading" class="grid gap-4 md:grid-cols-3">
      <div
        v-for="i in 6"
        :key="i"
        class="h-32 animate-pulse rounded-2xl bg-slate-200"
      />
    </div>
    <div
      v-else-if="error"
      class="rounded-2xl border border-red-200 bg-red-50 p-6 text-red-700"
    >
      {{ error }}
    </div>
    <div
      v-else-if="!cards.length"
      class="rounded-2xl border border-border bg-white p-10 text-center text-slate-500"
    >
      Aucune donnée disponible.
    </div>
    <div v-else class="grid gap-4 md:grid-cols-3">
      <article
        v-for="card in cards"
        :key="card.label"
        class="rounded-2xl border border-border bg-white p-6 shadow-sm"
      >
        <p class="text-sm font-medium capitalize text-slate-500">
          {{ card.label }}
        </p>
        <p class="mt-3 text-4xl font-bold tracking-tight">{{ card.value }}</p>
      </article>
    </div>
  </div>
</template>
