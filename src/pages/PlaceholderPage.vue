<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { AlertCircle, Check, ChevronLeft, ChevronRight, Edit3, Loader2, Plus, Search, Trash2, X, ExternalLink, Download } from 'lucide-vue-next'
import { 
  applicationsApi, companiesApi, documentsApi,
  evaluationsApi, internshipsApi, notificationsApi,
  offersApi, weeklyLogsApi,
} from '@/api/endpoints'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import type {
  Application, Company, Document, Evaluation,
  Internship, Notification, Offer, WeeklyLog,
} from '@/types/api'
import PageHeader    from '@/components/ui/PageHeader.vue'
import BaseCard      from '@/components/ui/BaseCard.vue'
import SearchBar     from '@/components/ui/SearchBar.vue'
import StatusBadge   from '@/components/ui/StatusBadge.vue'
import SkeletonCard  from '@/components/ui/SkeletonCard.vue'
import EmptyState    from '@/components/ui/EmptyState.vue'
import ErrorState    from '@/components/ui/ErrorState.vue'
import PaginationBar from '@/components/ui/PaginationBar.vue'

const route = useRoute()
const auth  = useAuthStore()
const toast = useToast()

/* ─── state ─────────────────────────────────────────── */
const loading = ref(false)
const saving  = ref(false)
const error   = ref('')
const search  = ref('')
const page    = ref(1)
const total   = ref(0)

const offers        = ref<Offer[]>([])
const applications  = ref<Application[]>([])
const internships   = ref<Internship[]>([])
const documents     = ref<Document[]>([])
const weeklyLogs    = ref<WeeklyLog[]>([])
const evaluations   = ref<Evaluation[]>([])
const notifications = ref<Notification[]>([])
const companies     = ref<Company[]>([])

const selectedOffer  = ref<Offer | null>(null)
const editingOfferId = ref<string | null>(null)
const coverLetter    = ref('')

const offerForm = reactive({
  company: '', title: '', description: '', location: '',
  required_skills: '', start_date: '', end_date: '', is_active: true,
})
const weeklyLogForm = reactive({
  internship: '', week_start: '', activities: '', blockers: '', next_steps: '',
})
const evaluationForm = reactive({
  internship: '', evaluation_type: 'ACADEMIC' as 'ACADEMIC' | 'PROFESSIONAL',
  score: 80, comment: '',
})

/* ─── helpers ────────────────────────────────────────── */
const activeView  = computed(() => String(route.name ?? ''))
const totalPages  = computed(() => Math.max(1, Math.ceil(total.value / 20)))
const isPaginated = computed(() =>
  ['offers','company-offers','applications','company-applications',
   'internships','university-internships','documents',
   'weekly-logs','evaluations','notifications'].includes(activeView.value)
)

function resetState() {
  error.value       = ''
  selectedOffer.value = null
  ;[applications, internships, documents, weeklyLogs,
    evaluations, notifications, offers, companies].forEach(r => (r.value = []))
  total.value = 0
}

function resetOfferForm(company = '') {
  Object.assign(offerForm, { company, title: '', description: '', location: '',
    required_skills: '', start_date: '', end_date: '', is_active: true })
  editingOfferId.value = null
}

function editOffer(o: Offer) {
  Object.assign(offerForm, {
    company: o.company, title: o.title, description: o.description,
    location: o.location ?? '', required_skills: o.required_skills ?? '',
    start_date: o.start_date ?? '', end_date: o.end_date ?? '',
    is_active: o.is_active ?? true,
  })
  editingOfferId.value = o.id
}

/* ─── loaders ────────────────────────────────────────── */
async function loadCompanies() {
  companies.value = (await companiesApi.list()).results
  if (!offerForm.company && companies.value[0]) offerForm.company = companies.value[0].id
}

async function loadOffers() {
  const r = await offersApi.list({ page: page.value, search: search.value || undefined })
  offers.value = r.results; total.value = r.count
}

async function loadApplications() {
  const r = await applicationsApi.list({ page: page.value, search: search.value || undefined })
  applications.value = r.results; total.value = r.count
}

async function loadInternships() {
  const r = await internshipsApi.list({ page: page.value, search: search.value || undefined })
  internships.value = r.results; total.value = r.count
  if (!weeklyLogForm.internship && r.results[0])   weeklyLogForm.internship   = r.results[0].id
  if (!evaluationForm.internship && r.results[0])  evaluationForm.internship  = r.results[0].id
}

async function loadDocuments() {
  const r = await documentsApi.list({ page: page.value, search: search.value || undefined })
  documents.value = r.results; total.value = r.count
}

async function loadWeeklyLogs() {
  const r = await weeklyLogsApi.list({ page: page.value, search: search.value || undefined })
  weeklyLogs.value = r.results; total.value = r.count
  if (!internships.value.length) {
    const ir = await internshipsApi.list()
    internships.value = ir.results
    if (!weeklyLogForm.internship && ir.results[0]) weeklyLogForm.internship = ir.results[0].id
  }
}

async function loadEvaluations() {
  const r = await evaluationsApi.list({ page: page.value })
  evaluations.value = r.results; total.value = r.count
  if (!internships.value.length) {
    const ir = await internshipsApi.list()
    internships.value = ir.results
    if (!evaluationForm.internship && ir.results[0]) evaluationForm.internship = ir.results[0].id
  }
}

async function loadNotifications() {
  const r = await notificationsApi.list({ page: page.value, search: search.value || undefined })
  notifications.value = r.results; total.value = r.count
}

async function loadOfferDetail() {
  selectedOffer.value = await offersApi.retrieve(String(route.params.id))
}

async function loadCurrentView() {
  loading.value = true;
  resetState();
  try {
    const v = activeView.value
    if (v === 'offers' || v === 'company-offers') { if (v === 'company-offers') await loadCompanies(); await loadOffers() }
    else if (v === 'offer-detail')       await loadOfferDetail()
    else if (['applications','company-applications'].includes(v))    await loadApplications()
    else if (['internships','university-internships'].includes(v))   await loadInternships()
    else if (v === 'documents')    await loadDocuments()
    else if (v === 'weekly-logs')  await loadWeeklyLogs()
    else if (v === 'evaluations')  await loadEvaluations()
    else if (v === 'notifications') await loadNotifications()
  } catch {
    error.value = 'Erreur lors du chargement.'
  } finally {
    loading.value = false
  }
}

/* ─── actions ────────────────────────────────────────── */
async function submitApplication() {
  if (!selectedOffer.value) return
  saving.value = true
  try {
    await applicationsApi.create({ offer: selectedOffer.value.id, cover_letter: coverLetter.value })
    toast.success('Candidature envoyée')
    coverLetter.value = ''
  } catch {
    toast.error('Erreur', 'La candidature n\'a pas pu être envoyée.')
  } finally { saving.value = false }
}

async function saveOffer() {
  saving.value = true
  try {
    const p = { ...offerForm, start_date: offerForm.start_date || null, end_date: offerForm.end_date || null }
    editingOfferId.value
      ? await offersApi.update(editingOfferId.value, p)
      : await offersApi.create(p)
    toast.success(editingOfferId.value ? 'Offre modifiée' : 'Offre créée')
    resetOfferForm(offerForm.company)
    await loadOffers()
  } catch {
    toast.error('Erreur', 'L\'offre n\'a pas pu être enregistrée.')
  } finally { saving.value = false }
}

async function deleteOffer(id: string) {
  saving.value = true
  try {
    await offersApi.remove(id); await loadOffers()
    toast.success('Offre supprimée')
  } catch {
    toast.error('Erreur', 'La suppression a échoué.')
  } finally { saving.value = false }
}

async function submitWeeklyLog() {
  saving.value = true
  try {
    await weeklyLogsApi.create({ ...weeklyLogForm })
    toast.success('Journal enregistré')
    Object.assign(weeklyLogForm, { week_start: '', activities: '', blockers: '', next_steps: '' })
    await loadWeeklyLogs()
  } catch {
    toast.error('Erreur', 'Le journal n\'a pas pu être enregistré.')
  } finally { saving.value = false }
}

async function submitEvaluation() {
  saving.value = true
  try {
    await evaluationsApi.create({ ...evaluationForm, score: Number(evaluationForm.score) })
    toast.success('Évaluation enregistrée')
    Object.assign(evaluationForm, { score: 80, comment: '' })
    await loadEvaluations()
  } catch {
    toast.error('Erreur', 'L\'évaluation n\'a pas pu être enregistrée.')
  } finally { saving.value = false }
}

async function markNotificationRead(n: Notification) {
  saving.value = true
  try {
    await notificationsApi.action(n.id, 'read'); await loadNotifications()
  } catch {
    toast.error('Erreur', 'La notification n\'a pas pu être mise à jour.')
  } finally { saving.value = false }
}

async function reviewDocument(doc: Document, action: 'approve' | 'reject') {
  saving.value = true
  try {
    await documentsApi.action(doc.id, action)
    toast.success(action === 'approve' ? 'Document approuvé' : 'Document rejeté')
    await loadDocuments()
  } catch {
    toast.error('Erreur', 'Le document n\'a pas pu être mis à jour.')
  } finally { saving.value = false }
}

async function reviewApplication(app: Application, action: 'accept' | 'reject') {
  saving.value = true
  try {
    await applicationsApi.action(app.id, action)
    toast.success(action === 'accept' ? 'Candidature acceptée' : 'Candidature rejetée')
    await loadApplications()
  } catch {
    toast.error('Erreur', 'La candidature n\'a pas pu être mise à jour.')
  } finally { saving.value = false }
}

watch(() => route.fullPath, () => { page.value = 1; resetOfferForm(); void loadCurrentView() })
watch(page, () => { if (isPaginated.value) void loadCurrentView() })
onMounted(loadCurrentView)

/* shared input class */
const inp = 'w-full rounded-xl border border-border px-3 py-2.5 text-sm focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-100'
const btn = {
  primary:   'rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-slate-800 disabled:opacity-50',
  secondary: 'rounded-xl border border-border px-4 py-2.5 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-50',
  danger:    'rounded-xl border border-red-200 px-4 py-2 text-sm font-medium text-red-700 transition-colors hover:bg-red-50',
  success:   'rounded-xl border border-emerald-200 px-4 py-2 text-sm font-medium text-emerald-700 transition-colors hover:bg-emerald-50',
}
</script>

<template>
  <div class="space-y-6">
    <PageHeader :title="String(route.meta.label ?? '')" eyebrow="Sprint Front 1" />

    <!-- No-API notice -->
    <BaseCard
      v-if="activeView === 'profile' || activeView === 'university-students'"
      class="rounded-2xl border border-amber-200 bg-amber-50 p-6 text-amber-900"
    >
      <div class="flex gap-3">
        <AlertCircle class="mt-0.5 h-5 w-5 shrink-0 text-amber-500" />
        <div>
          <p class="font-semibold text-amber-900">Endpoint backend non exposé</p>
          <p class="mt-1 text-sm text-amber-800">
            Aucun endpoint OpenAPI disponible pour ce module. L'interface n'affiche ni formulaire, ni données fictives.
          </p>
          <p v-if="activeView === 'profile'" class="mt-3 text-sm text-amber-800">
            <span class="font-medium">Session JWT :</span>
            {{ auth.user?.email ?? auth.user?.id ?? 'Utilisateur authentifié' }}
          </p>
        </div>
      </div>
    </BaseCard>

    <template v-else>

      <!-- Toolbar: SearchBar + Apply -->
      <div
        v-if="isPaginated"
        class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between"
      >
        <SearchBar v-model="search" @search="page = 1; loadCurrentView()" />
        <button :class="btn.secondary" @click="page = 1; loadCurrentView()">Appliquer</button>
      </div>

      <!-- Create weekly log form -->
      <BaseCard v-if="activeView === 'weekly-logs'">
        <h3 class="text-base font-semibold text-slate-900">Déposer un journal hebdomadaire</h3>
        <form class="mt-4 grid gap-4 md:grid-cols-2" @submit.prevent="submitWeeklyLog">
          <select v-model="weeklyLogForm.internship" required :class="inp">
            <option value="" disabled>Stage</option>
            <option v-for="i in internships" :key="i.id" :value="i.id">Stage {{ i.id.slice(0,8) }}…</option>
          </select>
          <input v-model="weeklyLogForm.week_start" required type="date" :class="inp" />
          <textarea v-model="weeklyLogForm.activities" required :class="inp + ' min-h-[7rem] md:col-span-2'" placeholder="Activités réalisées" />
          <textarea v-model="weeklyLogForm.blockers"   :class="inp + ' min-h-[5rem]'" placeholder="Blocages (optionnel)" />
          <textarea v-model="weeklyLogForm.next_steps" :class="inp + ' min-h-[5rem]'" placeholder="Prochaines étapes (optionnel)" />
          <div class="md:col-span-2">
            <button :class="btn.primary" :disabled="saving" type="submit">
              <Loader2 v-if="saving" class="mr-2 inline h-4 w-4 animate-spin" />
              Enregistrer le journal
            </button>
          </div>
        </form>
      </BaseCard>

      <!-- Create evaluation form -->
      <BaseCard v-if="activeView === 'evaluations'">
        <h3 class="text-base font-semibold text-slate-900">Créer une évaluation</h3>
        <form class="mt-4 grid gap-4 md:grid-cols-2" @submit.prevent="submitEvaluation">
          <select v-model="evaluationForm.internship" required :class="inp">
            <option value="" disabled>Stage</option>
            <option v-for="i in internships" :key="i.id" :value="i.id">Stage {{ i.id.slice(0,8) }}…</option>
          </select>
          <select v-model="evaluationForm.evaluation_type" :class="inp">
            <option value="ACADEMIC">Académique</option>
            <option value="PROFESSIONAL">Professionnelle</option>
          </select>
          <input v-model.number="evaluationForm.score" required type="number" min="0" max="100" :class="inp" placeholder="Score /100" />
          <textarea v-model="evaluationForm.comment" :class="inp + ' min-h-[5rem]'" placeholder="Commentaire (optionnel)" />
          <div class="md:col-span-2">
            <button :class="btn.primary" :disabled="saving" type="submit">
              <Loader2 v-if="saving" class="mr-2 inline h-4 w-4 animate-spin" />
              Enregistrer l'évaluation
            </button>
          </div>
        </form>
      </BaseCard>

      <!-- Company: create/edit offer form -->
      <BaseCard v-if="activeView === 'company-offers'">
        <h3 class="text-base font-semibold text-slate-900">
          {{ editingOfferId ? 'Modifier l\'offre' : 'Créer une offre' }}
        </h3>
        <form class="mt-4 grid gap-4 md:grid-cols-2" @submit.prevent="saveOffer">
          <select v-model="offerForm.company" required :class="inp">
            <option value="" disabled>Entreprise</option>
            <option v-for="c in companies" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
          <input v-model="offerForm.title" required :class="inp" placeholder="Titre du poste" />
          <input v-model="offerForm.location"        :class="inp" placeholder="Localisation" />
          <input v-model="offerForm.required_skills" :class="inp" placeholder="Compétences requises" />
          <input v-model="offerForm.start_date" type="date" :class="inp" />
          <input v-model="offerForm.end_date"   type="date" :class="inp" />
          <textarea v-model="offerForm.description" required :class="inp + ' min-h-[7rem] md:col-span-2'" placeholder="Description" />
          <div class="flex items-center gap-2 md:col-span-2">
            <button :class="btn.primary" :disabled="saving" type="submit">
              <Plus  v-if="!editingOfferId" class="mr-2 inline h-4 w-4" />
              <Edit3 v-else                class="mr-2 inline h-4 w-4" />
              Enregistrer
            </button>
            <button v-if="editingOfferId" type="button" :class="btn.secondary" @click="resetOfferForm(offerForm.company)">
              Annuler
            </button>
          </div>
        </form>
      </BaseCard>

      <!-- Loading skeleton -->
      <SkeletonCard v-if="loading" :count="4" />

      <!-- Error -->
      <ErrorState v-else-if="error" :message="error" @retry="loadCurrentView" />

      <!-- Offer detail -->
      <template v-else-if="activeView === 'offer-detail' && selectedOffer">
        <div class="grid gap-6 lg:grid-cols-[1fr_22rem]">
          <BaseCard padding="lg">
            <p class="text-sm font-medium text-slate-400">{{ selectedOffer.location || 'Localisation non renseignée' }}</p>
            <h3 class="mt-2 text-3xl font-bold tracking-tight text-slate-900">{{ selectedOffer.title }}</h3>
            <p class="mt-6 whitespace-pre-line text-sm leading-7 text-slate-700">{{ selectedOffer.description }}</p>
            <div v-if="selectedOffer.required_skills" class="mt-6 rounded-xl bg-slate-50 p-4 text-sm text-slate-600">
              <span class="font-medium">Compétences requises :</span> {{ selectedOffer.required_skills }}
      </div>
          </BaseCard>
          <BaseCard>
            <h3 class="font-semibold text-slate-900">Postuler</h3>
            <form class="mt-4 space-y-3" @submit.prevent="submitApplication">
              <textarea
                v-model="coverLetter"
                :class="inp + ' min-h-[10rem]'"
                placeholder="Lettre de motivation…"
              />
              <button :class="btn.primary + ' w-full justify-center'" :disabled="saving" type="submit">
                <Loader2 v-if="saving" class="mr-2 inline h-4 w-4 animate-spin" />
                Envoyer la candidature
              </button>
            </form>
          </BaseCard>
      </div>
      </template>

      <!-- Offers list -->
      <template v-else-if="['offers','company-offers'].includes(activeView)">
        <div v-if="offers.length" class="grid gap-4 md:grid-cols-2">
          <article
            v-for="offer in offers"
            :key="offer.id"
            class="flex flex-col rounded-2xl border border-border bg-white p-6 shadow-sm transition-shadow hover:shadow-md"
          >
            <div class="flex items-start justify-between gap-3">
              <div class="min-w-0">
                <p class="text-xs font-medium text-slate-400">{{ offer.location || 'Localisation non renseignée' }}</p>
                <h3 class="mt-1 truncate text-lg font-semibold text-slate-900">{{ offer.title }}</h3>
      </div>
              <span
                class="shrink-0 rounded-full px-2.5 py-0.5 text-xs font-medium"
                :class="offer.is_active ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-500'"
              >
                {{ offer.is_active ? 'Active' : 'Inactive' }}
              </span>
      </div>
            <p class="mt-3 flex-1 line-clamp-3 text-sm leading-relaxed text-slate-600">{{ offer.description }}</p>
            <div class="mt-5 flex flex-wrap items-center gap-2 border-t border-border pt-4">
              <RouterLink :to="`/offers/${offer.id}`" :class="btn.primary">Voir l'offre</RouterLink>
              <template v-if="activeView === 'company-offers'">
                <button :class="btn.secondary" @click="editOffer(offer)">
                  <Edit3 class="mr-1.5 inline h-3.5 w-3.5" /> Modifier
                </button>
                <button :class="btn.danger" @click="deleteOffer(offer.id)">
                  <Trash2 class="mr-1.5 inline h-3.5 w-3.5" /> Supprimer
                </button>
              </template>
            </div>
          </article>
      </div>
        <EmptyState v-else title="Aucune offre" description="Aucune offre ne correspond à votre recherche." />
      </template>

      <!-- Applications list -->
      <template v-else-if="['applications','company-applications'].includes(activeView)">
        <div v-if="applications.length" class="space-y-3">
          <article
            v-for="app in applications"
            :key="app.id"
            class="flex items-center gap-4 rounded-2xl border border-border bg-white p-5 shadow-sm"
          >
            <div class="min-w-0 flex-1">
              <p class="text-xs text-slate-400">ID candidature</p>
              <p class="truncate font-mono text-sm font-medium text-slate-700">{{ app.id }}</p>
            </div>
            <StatusBadge :status="String(app.status)" />
            <div class="flex shrink-0 gap-2">
              <RouterLink :to="`/offers/${app.offer}`" :class="btn.secondary" title="Voir l'offre">
                <ExternalLink class="h-4 w-4" />
              </RouterLink>
              <template v-if="activeView === 'company-applications'">
                <button :class="btn.success" @click="reviewApplication(app, 'accept')">
                  <Check class="mr-1.5 inline h-3.5 w-3.5" /> Accepter
                </button>
                <button :class="btn.danger" @click="reviewApplication(app, 'reject')">
                  <X class="mr-1.5 inline h-3.5 w-3.5" /> Rejeter
                </button>
              </template>
            </div>
          </article>
      </div>
        <EmptyState v-else title="Aucune candidature" />
      </template>

      <!-- Documents list -->
      <template v-else-if="activeView === 'documents'">
        <div v-if="documents.length" class="space-y-3">
          <article
            v-for="doc in documents"
            :key="doc.id"
            class="rounded-2xl border border-border bg-white p-5 shadow-sm"
          >
            <div class="flex items-start gap-4">
              <div class="min-w-0 flex-1">
                <div class="flex items-center gap-2">
                  <p class="font-semibold text-slate-900">{{ doc.title }}</p>
                  <StatusBadge :status="String(doc.status)" />
                  <span class="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-500">{{ doc.document_type }}</span>
                </div>
                <p v-if="doc.comment" class="mt-1 text-sm text-slate-500">{{ doc.comment }}</p>
              </div>
              <div class="flex shrink-0 gap-2">
                <a :href="doc.file" target="_blank" rel="noreferrer" :class="btn.secondary" title="Télécharger">
                  <Download class="h-4 w-4" />
                </a>
                <button :class="btn.success" @click="reviewDocument(doc, 'approve')">
                  <Check class="mr-1.5 inline h-3.5 w-3.5" /> Approuver
                </button>
                <button :class="btn.danger" @click="reviewDocument(doc, 'reject')">
                  <X class="mr-1.5 inline h-3.5 w-3.5" /> Rejeter
                </button>
              </div>
            </div>
          </article>
        </div>
        <EmptyState v-else title="Aucun document" />
      </template>

      <!-- Weekly logs list -->
      <template v-else-if="activeView === 'weekly-logs'">
        <div v-if="weeklyLogs.length" class="space-y-3">
        <article
            v-for="log in weeklyLogs"
            :key="log.id"
          class="rounded-2xl border border-border bg-white p-5 shadow-sm"
        >
            <p class="text-xs font-semibold uppercase tracking-widest text-slate-400">
              Semaine du {{ log.week_start }}
            </p>
            <p class="mt-2 whitespace-pre-line text-sm leading-relaxed text-slate-700">{{ log.activities }}</p>
            <p v-if="log.blockers" class="mt-2 text-sm text-red-600">
              <span class="font-medium">Blocages :</span> {{ log.blockers }}
            </p>
            <p v-if="log.next_steps" class="mt-1 text-sm text-indigo-600">
              <span class="font-medium">Suite :</span> {{ log.next_steps }}
            </p>
          </article>
        </div>
        <EmptyState v-else title="Aucun journal" description="Déposez votre premier journal hebdomadaire ci-dessus." />
      </template>

      <!-- Evaluations list -->
      <template v-else-if="activeView === 'evaluations'">
        <div v-if="evaluations.length" class="space-y-3">
          <article
            v-for="ev in evaluations"
            :key="ev.id"
            class="rounded-2xl border border-border bg-white p-5 shadow-sm"
          >
            <div class="flex items-center justify-between gap-4">
            <div>
                <p class="text-xs font-semibold uppercase tracking-widest text-slate-400">{{ ev.evaluation_type }}</p>
                <p v-if="ev.comment" class="mt-1 text-sm text-slate-600">{{ ev.comment }}</p>
              </div>
              <p class="shrink-0 text-3xl font-bold tabular-nums text-slate-900">
                {{ ev.score }}<span class="text-base font-normal text-slate-400">/100</span>
              </p>
            </div>
          </article>
        </div>
        <EmptyState v-else title="Aucune évaluation" />
      </template>

      <!-- Notifications list -->
      <template v-else-if="activeView === 'notifications'">
        <div v-if="notifications.length" class="space-y-3">
          <article
            v-for="n in notifications"
            :key="n.id"
            class="flex items-start gap-4 rounded-2xl border bg-white p-5 shadow-sm transition-colors"
            :class="n.is_read ? 'border-border' : 'border-indigo-200 bg-indigo-50/30'"
          >
            <div class="mt-1 flex h-2 w-2 shrink-0 items-center justify-center">
              <span v-if="!n.is_read" class="h-2 w-2 rounded-full bg-indigo-500" aria-label="Non lue" />
            </div>
            <div class="min-w-0 flex-1">
              <p class="font-semibold text-slate-900">{{ n.title }}</p>
              <p class="mt-0.5 text-sm text-slate-600">{{ n.message }}</p>
            </div>
            <button
              v-if="!n.is_read"
              :class="btn.secondary + ' shrink-0 text-xs'"
              @click="markNotificationRead(n)"
            >
              Marquer lue
            </button>
          </article>
        </div>
        <EmptyState v-else title="Aucune notification" description="Vous êtes à jour." />
      </template>

      <!-- Internships list -->
      <template
        v-else-if="['internships','university-internships'].includes(activeView)"
      >
        <div v-if="internships.length" class="space-y-3">
          <article
            v-for="i in internships"
            :key="i.id"
            class="flex items-center gap-4 rounded-2xl border border-border bg-white p-5 shadow-sm"
          >
            <div class="min-w-0 flex-1">
              <p class="font-mono text-xs text-slate-400">{{ i.id.slice(0,8) }}…</p>
              <p class="mt-0.5 text-sm text-slate-600">
                {{ i.start_date || '—' }} → {{ i.end_date || '—' }}
            </p>
          </div>
            <StatusBadge :status="String(i.status)" />
        </article>
        </div>
        <EmptyState v-else title="Aucun stage" />
      </template>

      <!-- Pagination -->
      <PaginationBar
        v-if="isPaginated"
        :page="page"
        :total="total"
        @update:page="p => { page = p }"
      />

    </template>
  </div>
</template>
