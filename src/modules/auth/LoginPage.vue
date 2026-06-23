<script setup lang="ts">
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Loader2 } from "lucide-vue-next";
import { useAuthStore } from "@/stores/auth";
const email = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");
const auth = useAuthStore();
const router = useRouter();
const route = useRoute();
const inp = 'mt-2 w-full rounded-xl border border-border px-4 py-3 text-sm text-slate-900 placeholder:text-slate-400 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-100'

async function submit() {
  loading.value = true;
  error.value = "";
  try {
    await auth.login({ email: email.value, password: password.value });
    router.push(String(route.query.redirect ?? "/app/dashboard"));
  } catch (e) {
    error.value = "Identifiants invalides ou session indisponible.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <main
    class="grid min-h-screen grid-cols-1 bg-slate-50 lg:grid-cols-[1.1fr_0.9fr]">
    
    <!-- Left panel -->
    <section
      aria-hidden="true"
      class="relative hidden overflow-hidden border-r border-border bg-slate-950 p-12 lg:flex lg:flex-col lg:justify-between"
    >
      <!-- Subtle grid texture -->
      <div
        class="pointer-events-none absolute inset-0 opacity-5"
        style="background-image: linear-gradient(rgba(255,255,255,.15) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.15) 1px, transparent 1px); background-size: 32px 32px;"
      />

      <!-- Accent blob -->
      <div
        class="pointer-events-none absolute -right-32 -top-32 h-96 w-96 rounded-full bg-indigo-600/20 blur-3xl"
      />
      <div
        class="pointer-events-none absolute -bottom-24 -left-24 h-72 w-72 rounded-full bg-violet-600/10 blur-3xl"
      />

      <div class="relative">
        <div class="flex items-center gap-2.5">
          <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-500 text-sm font-bold text-white">
            EC
          </div>
          <span class="text-base font-bold text-white">E-CON</span>
        </div>

        <div class="mt-20 max-w-xl">
          <p class="text-xs font-semibold uppercase tracking-[0.25em] text-indigo-400">
            Plateforme académique
          </p>
          <h1 class="mt-4 text-5xl font-bold leading-[1.1] tracking-tight text-white">
            Pilotez les stages avec clarté et sécurité.
          </h1>
          <p class="mt-6 text-base leading-relaxed text-slate-400">
            Interface connectée aux endpoints backend réels. Authentification JWT,
            contrôle d'accès par rôle et flux métier complets.
          </p>
        </div>

        <!-- Feature pills -->
        <div class="mt-10 flex flex-wrap gap-2">
          <span
            v-for="feat in ['Candidatures', 'Stages', 'Documents', 'Évaluations', 'Notifications']"
            :key="feat"
            class="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-400"
          >{{ feat }}</span>
        </div>
      </div>

      <p class="relative text-xs text-slate-600">
        Design system institutionnel · WCAG 2.1 AA
      </p>
    </section>

    <!-- Right panel: form -->
    <section class="flex items-center justify-center p-6">
      <div class="w-full max-w-md">

        <!-- Mobile logo -->
        <div class="mb-8 flex items-center gap-2 lg:hidden">
          <div class="flex h-7 w-7 items-center justify-center rounded-lg bg-indigo-600 text-xs font-bold text-white">
            EC
          </div>
          <span class="font-bold text-slate-900">E-CON</span>
        </div>

        <div class="rounded-2xl border border-border bg-white p-8 shadow-sm">
          <div class="flex items-center gap-2">
            <ShieldCheck class="h-5 w-5 text-indigo-500" />
            <h2 class="text-xl font-bold tracking-tight text-slate-900">Connexion sécurisée</h2>
          </div>
          <p class="mt-1 text-sm text-slate-400">Utilisez votre compte E-CON institutionnel.</p>

          <form class="mt-7 space-y-4" @submit.prevent="submit">
            <label class="block text-sm font-medium text-slate-700">
              Adresse email
              <input
            v-model="email"
            type="email"
            autocomplete="email"
            required
                placeholder="vous@université.fr"
                :class="inp"
              />
            </label>

            <label class="block text-sm font-medium text-slate-700">
              Mot de passe
              <input
            v-model="password"
            type="password"
            autocomplete="current-password"
            required
                placeholder="••••••••"
                :class="inp"
              />
            </label>

            <Transition name="fade">
              <div
          v-if="error"
                role="alert"
                class="flex items-start gap-2 rounded-xl border border-red-200 bg-red-50 p-3"
              >
                <span class="mt-0.5 h-4 w-4 shrink-0 text-red-500">!</span>
                <p class="text-sm text-red-700">{{ error }}</p>
              </div>
            </Transition>

        <button
              type="submit"
              class="mt-2 flex w-full items-center justify-center rounded-xl bg-indigo-600 px-4 py-3 text-sm font-semibold text-white transition-colors hover:bg-indigo-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-60"
          :disabled="loading"
        >
              <Loader2 v-if="loading" class="mr-2 h-4 w-4 animate-spin" />
              {{ loading ? 'Connexion…' : 'Se connecter' }}
        </button>
      </form>
        </div>

        <p class="mt-4 text-center text-xs text-slate-400">
          Accès réservé aux membres de l'écosystème E-CON.
        </p>
      </div>
    </section>

  </main>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.18s; }
.fade-enter-from, .fade-leave-to       { opacity: 0; }
</style>