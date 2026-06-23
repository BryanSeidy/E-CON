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
    class="grid min-h-screen grid-cols-1 bg-slate-50 lg:grid-cols-[1.1fr_0.9fr]"
  >
    <section
      class="hidden border-r border-border bg-white p-12 lg:flex lg:flex-col lg:justify-between"
    >
      <div>
        <div class="text-2xl font-bold">E-CON</div>
        <div class="mt-20 max-w-xl">
          <p
            class="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500"
          >
            Plateforme académique
          </p>
          <h1 class="mt-4 text-5xl font-bold tracking-tight">
            Pilotez les stages avec une expérience claire et sécurisée.
          </h1>
          <p class="mt-5 text-lg leading-8 text-slate-600">
            Frontend connecté uniquement aux endpoints réels du backend MVP,
            avec authentification JWT et garde RBAC.
          </p>
        </div>
      </div>
      <p class="text-sm text-slate-500">
        Design system premium, institutionnel et accessible.
      </p>
    </section>
    <section class="flex items-center justify-center p-6">
      <form
        class="w-full max-w-md rounded-2xl border border-border bg-white p-8 shadow-sm"
        @submit.prevent="submit"
      >
        <h2 class="text-2xl font-semibold tracking-tight">Connexion</h2>
        <p class="mt-2 text-sm text-slate-500">Utilisez votre compte E-CON.</p>
        <label class="mt-8 block text-sm font-medium"
          >Email<input
            v-model="email"
            type="email"
            autocomplete="email"
            required
            class="mt-2 w-full rounded-xl border border-border px-4 py-3 outline-none focus:border-slate-900" /></label
        ><label class="mt-4 block text-sm font-medium"
          >Mot de passe<input
            v-model="password"
            type="password"
            autocomplete="current-password"
            required
            class="mt-2 w-full rounded-xl border border-border px-4 py-3 outline-none focus:border-slate-900"
        /></label>
        <p
          v-if="error"
          class="mt-4 rounded-xl bg-red-50 p-3 text-sm text-red-700"
        >
          {{ error }}
        </p>
        <button
          class="mt-6 flex w-full items-center justify-center rounded-xl bg-slate-950 px-4 py-3 font-semibold text-white disabled:opacity-60"
          :disabled="loading"
        >
          <Loader2 v-if="loading" class="mr-2 h-4 w-4 animate-spin" />Se
          connecter
        </button>
      </form>
    </section>
  </main>
</template>
