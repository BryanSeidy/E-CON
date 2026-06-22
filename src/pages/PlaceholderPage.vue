<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from "vue";
import { RouterLink, useRoute } from "vue-router";
import {
  AlertCircle,
  Check,
  ChevronLeft,
  ChevronRight,
  Edit3,
  Loader2,
  Plus,
  Search,
  Trash2,
  X,
} from "lucide-vue-next";
import {
  applicationsApi,
  companiesApi,
  internshipsApi,
  offersApi,
} from "@/api/endpoints";
import { useAuthStore } from "@/stores/auth";
import type { Application, Company, Internship, Offer } from "@/types/api";

const route = useRoute();
const auth = useAuthStore();
const loading = ref(false);
const saving = ref(false);
const error = ref("");
const search = ref("");
const page = ref(1);
const total = ref(0);
const offers = ref<Offer[]>([]);
const applications = ref<Application[]>([]);
const internships = ref<Internship[]>([]);
const companies = ref<Company[]>([]);
const selectedOffer = ref<Offer | null>(null);
const editingOfferId = ref<string | null>(null);
const coverLetter = ref("");
const offerForm = reactive({
  company: "",
  title: "",
  description: "",
  location: "",
  required_skills: "",
  start_date: "",
  end_date: "",
  is_active: true,
});
const activeView = computed(() => String(route.name ?? ""));
const isList = computed(() =>
  ["offers", "company-offers"].includes(activeView.value),
);
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / 20)));

function resetState() {
  error.value = "";
  selectedOffer.value = null;
  applications.value = [];
  internships.value = [];
  offers.value = [];
  total.value = 0;
}
function setError(message = "Une erreur est survenue pendant le chargement.") {
  error.value = message;
}
function resetOfferForm(company = "") {
  Object.assign(offerForm, {
    company,
    title: "",
    description: "",
    location: "",
    required_skills: "",
    start_date: "",
    end_date: "",
    is_active: true,
  });
  editingOfferId.value = null;
}
function editOffer(offer: Offer) {
  Object.assign(offerForm, {
    company: offer.company,
    title: offer.title,
    description: offer.description,
    location: offer.location ?? "",
    required_skills: offer.required_skills ?? "",
    start_date: offer.start_date ?? "",
    end_date: offer.end_date ?? "",
    is_active: offer.is_active ?? true,
  });
  editingOfferId.value = offer.id;
}

async function loadCompanies() {
  companies.value = (await companiesApi.list()).results;
  if (!offerForm.company && companies.value[0])
    offerForm.company = companies.value[0].id;
}
async function loadOffers() {
  const response = await offersApi.list({
    page: page.value,
    search: search.value || undefined,
  });
  offers.value = response.results;
  total.value = response.count;
}
async function loadApplications() {
  const response = await applicationsApi.list({
    page: page.value,
    search: search.value || undefined,
  });
  applications.value = response.results;
  total.value = response.count;
}
async function loadInternships() {
  const response = await internshipsApi.list({
    page: page.value,
    search: search.value || undefined,
  });
  internships.value = response.results;
  total.value = response.count;
}
async function loadOfferDetail() {
  selectedOffer.value = await offersApi.retrieve(String(route.params.id));
}
async function loadCurrentView() {
  loading.value = true;
  resetState();
  try {
    if (
      activeView.value === "offers" ||
      activeView.value === "company-offers"
    ) {
      if (activeView.value === "company-offers") await loadCompanies();
      await loadOffers();
    }
    if (activeView.value === "offer-detail") await loadOfferDetail();
    if (["applications", "company-applications"].includes(activeView.value))
      await loadApplications();
    if (["internships", "university-internships"].includes(activeView.value))
      await loadInternships();
  } catch {
    setError();
  } finally {
    loading.value = false;
  }
}
async function submitApplication() {
  if (!selectedOffer.value) return;
  saving.value = true;
  try {
    await applicationsApi.create({
      offer: selectedOffer.value.id,
      cover_letter: coverLetter.value,
    });
    coverLetter.value = "";
  } catch {
    setError("La candidature n’a pas pu être envoyée.");
  } finally {
    saving.value = false;
  }
}
async function saveOffer() {
  saving.value = true;
  try {
    const payload = {
      ...offerForm,
      start_date: offerForm.start_date || null,
      end_date: offerForm.end_date || null,
    };
    editingOfferId.value
      ? await offersApi.update(editingOfferId.value, payload)
      : await offersApi.create(payload);
    resetOfferForm(offerForm.company);
    await loadOffers();
  } catch {
    setError("L’offre n’a pas pu être enregistrée.");
  } finally {
    saving.value = false;
  }
}
async function deleteOffer(id: string) {
  saving.value = true;
  try {
    await offersApi.remove(id);
    await loadOffers();
  } catch {
    setError("L’offre n’a pas pu être supprimée.");
  } finally {
    saving.value = false;
  }
}
async function reviewApplication(
  application: Application,
  action: "accept" | "reject",
) {
  saving.value = true;
  try {
    await applicationsApi.action(application.id, action);
    await loadApplications();
  } catch {
    setError("La candidature n’a pas pu être mise à jour.");
  } finally {
    saving.value = false;
  }
}
function nextPage() {
  if (page.value < totalPages.value) page.value += 1;
}
function previousPage() {
  if (page.value > 1) page.value -= 1;
}

watch(
  () => route.fullPath,
  () => {
    page.value = 1;
    resetOfferForm();
    void loadCurrentView();
  },
);
watch([page], () => {
  if (
    isList.value ||
    [
      "applications",
      "company-applications",
      "internships",
      "university-internships",
    ].includes(activeView.value)
  )
    void loadCurrentView();
});
onMounted(loadCurrentView);
</script>

<template>
  <section class="space-y-6">
    <div class="rounded-2xl border border-border bg-white p-6 shadow-sm">
      <p class="text-sm font-semibold uppercase tracking-wide text-slate-500">
        Sprint Front 1
      </p>
      <h2 class="mt-2 text-3xl font-bold tracking-tight">
        {{ route.meta.label }}
      </h2>
      <p class="mt-3 max-w-3xl text-slate-600">
        Ecran connecté aux clients API générés depuis l’OpenAPI backend. Les
        sections sans endpoint backend exposé affichent une limitation
        explicite.
      </p>
    </div>

    <div
      v-if="activeView === 'profile' || activeView === 'university-students'"
      class="rounded-2xl border border-amber-200 bg-amber-50 p-6 text-amber-900"
    >
      <div class="flex gap-3">
        <AlertCircle class="mt-0.5 h-5 w-5 shrink-0" />
        <div>
          <h3 class="font-semibold">Endpoint backend non exposé</h3>
          <p class="mt-1 text-sm">
            La documentation OpenAPI disponible ne contient pas d’endpoint
            Accounts/Profile/Students. Cette interface n’invente donc ni modèle,
            ni formulaire d’édition, ni données mockées.
          </p>
          <p v-if="activeView === 'profile'" class="mt-4 text-sm">
            <span class="font-medium">Session JWT locale :</span>
            {{ auth.user?.email || auth.user?.id || "Utilisateur authentifié" }}
          </p>
        </div>
      </div>
    </div>

    <template v-else>
      <div
        v-if="
          [
            'offers',
            'company-offers',
            'applications',
            'company-applications',
            'internships',
            'university-internships',
          ].includes(activeView)
        "
        class="flex flex-col gap-3 rounded-2xl border border-border bg-white p-4 md:flex-row md:items-center md:justify-between"
      >
        <label class="relative block w-full md:max-w-md"
          ><Search class="absolute left-3 top-3 h-4 w-4 text-slate-400" /><input
            v-model="search"
            class="w-full rounded-xl border border-border py-2.5 pl-10 pr-3 text-sm"
            placeholder="Rechercher"
            @keyup.enter="
              page = 1;
              loadCurrentView();
            "
        /></label>
        <button
          class="rounded-xl border border-border px-4 py-2 text-sm font-medium"
          @click="
            page = 1;
            loadCurrentView();
          "
        >
          Appliquer
        </button>
      </div>

      <div
        v-if="activeView === 'company-offers'"
        class="rounded-2xl border border-border bg-white p-6 shadow-sm"
      >
        <h3 class="text-lg font-semibold">
          {{ editingOfferId ? "Modifier une offre" : "Créer une offre" }}
        </h3>
        <form
          class="mt-4 grid gap-4 md:grid-cols-2"
          @submit.prevent="saveOffer"
        >
          <select
            v-model="offerForm.company"
            required
            class="rounded-xl border border-border px-3 py-2.5 text-sm"
          >
            <option value="" disabled>Entreprise</option>
            <option
              v-for="company in companies"
              :key="company.id"
              :value="company.id"
            >
              {{ company.name }}
            </option>
          </select>
          <input
            v-model="offerForm.title"
            required
            class="rounded-xl border border-border px-3 py-2.5 text-sm"
            placeholder="Titre"
          />
          <input
            v-model="offerForm.location"
            class="rounded-xl border border-border px-3 py-2.5 text-sm"
            placeholder="Localisation"
          />
          <input
            v-model="offerForm.required_skills"
            class="rounded-xl border border-border px-3 py-2.5 text-sm"
            placeholder="Compétences requises"
          />
          <input
            v-model="offerForm.start_date"
            type="date"
            class="rounded-xl border border-border px-3 py-2.5 text-sm"
          />
          <input
            v-model="offerForm.end_date"
            type="date"
            class="rounded-xl border border-border px-3 py-2.5 text-sm"
          />
          <textarea
            v-model="offerForm.description"
            required
            class="min-h-28 rounded-xl border border-border px-3 py-2.5 text-sm md:col-span-2"
            placeholder="Description"
          />
          <div class="flex items-center gap-3 md:col-span-2">
            <button
              class="rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-60"
              :disabled="saving"
            >
              <Plus v-if="!editingOfferId" class="mr-2 inline h-4 w-4" /><Edit3
                v-else
                class="mr-2 inline h-4 w-4"
              />Enregistrer</button
            ><button
              v-if="editingOfferId"
              type="button"
              class="rounded-xl border border-border px-4 py-2.5 text-sm"
              @click="resetOfferForm(offerForm.company)"
            >
              Annuler
            </button>
          </div>
        </form>
      </div>

      <div v-if="loading" class="grid gap-4 md:grid-cols-2">
        <div
          v-for="i in 4"
          :key="i"
          class="h-40 animate-pulse rounded-2xl bg-slate-200"
        />
      </div>
      <div
        v-else-if="error"
        class="rounded-2xl border border-red-200 bg-red-50 p-6 text-red-700"
      >
        {{ error }}
      </div>

      <div
        v-else-if="activeView === 'offer-detail' && selectedOffer"
        class="grid gap-6 lg:grid-cols-[1fr_24rem]"
      >
        <article
          class="rounded-2xl border border-border bg-white p-8 shadow-sm"
        >
          <p class="text-sm font-medium text-slate-500">
            {{ selectedOffer.location || "Localisation non renseignée" }}
          </p>
          <h3 class="mt-2 text-3xl font-bold">{{ selectedOffer.title }}</h3>
          <p class="mt-6 whitespace-pre-line leading-7 text-slate-700">
            {{ selectedOffer.description }}
          </p>
          <div class="mt-6 rounded-xl bg-slate-50 p-4 text-sm text-slate-600">
            <span class="font-medium">Compétences :</span>
            {{ selectedOffer.required_skills || "Non renseignées" }}
          </div>
        </article>
        <form
          class="rounded-2xl border border-border bg-white p-6 shadow-sm"
          @submit.prevent="submitApplication"
        >
          <h3 class="font-semibold">Candidater</h3>
          <textarea
            v-model="coverLetter"
            class="mt-4 min-h-40 w-full rounded-xl border border-border p-3 text-sm"
            placeholder="Lettre de motivation"
          /><button
            class="mt-4 w-full rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-60"
            :disabled="saving"
          >
            <Loader2
              v-if="saving"
              class="mr-2 inline h-4 w-4 animate-spin"
            />Envoyer la candidature
          </button>
        </form>
      </div>

      <div
        v-else-if="['offers', 'company-offers'].includes(activeView)"
        class="grid gap-4 md:grid-cols-2"
      >
        <article
          v-for="offer in offers"
          :key="offer.id"
          class="rounded-2xl border border-border bg-white p-6 shadow-sm"
        >
          <div class="flex items-start justify-between gap-4">
            <div>
              <p class="text-sm text-slate-500">
                {{ offer.location || "Localisation non renseignée" }}
              </p>
              <h3 class="mt-1 text-xl font-semibold">{{ offer.title }}</h3>
            </div>
            <span
              class="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium"
              >{{ offer.is_active ? "Active" : "Inactive" }}</span
            >
          </div>
          <p class="mt-4 line-clamp-3 text-sm leading-6 text-slate-600">
            {{ offer.description }}
          </p>
          <div class="mt-5 flex flex-wrap gap-2">
            <RouterLink
              class="rounded-xl bg-slate-950 px-4 py-2 text-sm font-semibold text-white"
              :to="`/offers/${offer.id}`"
              >Voir</RouterLink
            ><template v-if="activeView === 'company-offers'"
              ><button
                class="rounded-xl border border-border px-4 py-2 text-sm"
                @click="editOffer(offer)"
              >
                <Edit3 class="mr-2 inline h-4 w-4" />Modifier</button
              ><button
                class="rounded-xl border border-red-200 px-4 py-2 text-sm text-red-700"
                @click="deleteOffer(offer.id)"
              >
                <Trash2 class="mr-2 inline h-4 w-4" />Supprimer
              </button></template
            >
          </div>
        </article>
        <div
          v-if="!offers.length"
          class="rounded-2xl border border-border bg-white p-10 text-center text-slate-500 md:col-span-2"
        >
          Aucune offre trouvée.
        </div>
      </div>

      <div
        v-else-if="
          ['applications', 'company-applications'].includes(activeView)
        "
        class="space-y-3"
      >
        <article
          v-for="application in applications"
          :key="application.id"
          class="rounded-2xl border border-border bg-white p-5 shadow-sm"
        >
          <div
            class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between"
          >
            <div>
              <p class="text-sm text-slate-500">Candidature</p>
              <h3 class="font-semibold">{{ application.id }}</h3>
              <p class="mt-1 text-sm text-slate-600">
                Statut : {{ application.status }}
              </p>
            </div>
            <div class="flex flex-wrap gap-2">
              <RouterLink
                class="rounded-xl border border-border px-4 py-2 text-sm"
                :to="`/offers/${application.offer}`"
                >Offre</RouterLink
              ><template v-if="activeView === 'company-applications'"
                ><button
                  class="rounded-xl border border-emerald-200 px-4 py-2 text-sm text-emerald-700"
                  @click="reviewApplication(application, 'accept')"
                >
                  <Check class="mr-2 inline h-4 w-4" />Accepter</button
                ><button
                  class="rounded-xl border border-red-200 px-4 py-2 text-sm text-red-700"
                  @click="reviewApplication(application, 'reject')"
                >
                  <X class="mr-2 inline h-4 w-4" />Rejeter
                </button></template
              >
            </div>
          </div>
        </article>
        <div
          v-if="!applications.length"
          class="rounded-2xl border border-border bg-white p-10 text-center text-slate-500"
        >
          Aucune candidature trouvée.
        </div>
      </div>

      <div
        v-else-if="
          ['internships', 'university-internships'].includes(activeView)
        "
        class="space-y-3"
      >
        <article
          v-for="internship in internships"
          :key="internship.id"
          class="rounded-2xl border border-border bg-white p-5 shadow-sm"
        >
          <div
            class="flex flex-col gap-2 md:flex-row md:items-center md:justify-between"
          >
            <div>
              <h3 class="font-semibold">Stage {{ internship.id }}</h3>
              <p class="text-sm text-slate-600">
                Statut : {{ internship.status }}
              </p>
            </div>
            <p class="text-sm text-slate-500">
              {{ internship.start_date || "Début non renseigné" }} —
              {{ internship.end_date || "Fin non renseignée" }}
            </p>
          </div>
        </article>
        <div
          v-if="!internships.length"
          class="rounded-2xl border border-border bg-white p-10 text-center text-slate-500"
        >
          Aucun stage trouvé.
        </div>
      </div>

      <div
        v-if="
          [
            'offers',
            'company-offers',
            'applications',
            'company-applications',
            'internships',
            'university-internships',
          ].includes(activeView) && total > 20
        "
        class="flex items-center justify-between rounded-2xl border border-border bg-white p-4"
      >
        <button
          class="rounded-xl border border-border px-3 py-2 text-sm disabled:opacity-50"
          :disabled="page === 1"
          @click="previousPage"
        >
          <ChevronLeft class="mr-1 inline h-4 w-4" />Précédent</button
        ><span class="text-sm text-slate-500"
          >Page {{ page }} sur {{ totalPages }}</span
        ><button
          class="rounded-xl border border-border px-3 py-2 text-sm disabled:opacity-50"
          :disabled="page === totalPages"
          @click="nextPage"
        >
          Suivant<ChevronRight class="ml-1 inline h-4 w-4" />
        </button>
      </div>
    </template>
  </section>
</template>
