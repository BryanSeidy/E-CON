<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import {
  Check,
  Download,
  Loader2,
  Search,
  Upload,
  X,
} from 'lucide-vue-next'
import { documentsApi, internshipsApi, offersApi } from '@/api/endpoints'
import ListPagination from '@/components/ui/ListPagination.vue'
import PageStates from '@/components/ui/PageStates.vue'
import { useAuthStore } from '@/stores/auth'
import type {
  Document,
  DocumentStatusEnum,
  DocumentTypeEnum,
  Internship,
} from '@/types/api'
import {
  documentStatusClass,
  documentStatusLabel,
  documentTypeLabel,
  internshipLabel,
} from '@/utils/labels'

const PAGE_SIZE = 20
const REVIEWER_ROLES = new Set([
  'COMPANY_MEMBER',
  'ACADEMIC_SUPERVISOR',
  'HEAD_OF_PROGRAM',
  'UNIVERSITY_ADMIN',
  'SUPER_ADMIN',
])
const REVIEWABLE_STATUSES = new Set<DocumentStatusEnum>(['UPLOADED', 'IN_REVIEW'])

const auth = useAuthStore()
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const search = ref('')
const statusFilter = ref('')
const typeFilter = ref('')
const page = ref(1)
const total = ref(0)
const documents = ref<Document[]>([])
const internships = ref<Internship[]>([])
const offerTitles = ref<Record<string, string>>({})

const uploadForm = reactive({
  internship: '',
  document_type: 'CV' as DocumentTypeEnum,
  title: '',
  comment: '',
})
const selectedFile = ref<File | null>(null)
const reviewComment = ref('')
const reviewingId = ref<string | null>(null)

const canUpload = computed(() => auth.role === 'STUDENT')
const canReview = computed(() => REVIEWER_ROLES.has(auth.role ?? ''))
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / PAGE_SIZE)))

function resetUploadForm() {
  Object.assign(uploadForm, {
    internship: uploadForm.internship,
    document_type: 'CV' as DocumentTypeEnum,
    title: '',
    comment: '',
  })
  selectedFile.value = null
}

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  selectedFile.value = input.files?.[0] ?? null
}

function canReviewDocument(document: Document): boolean {
  return (
    canReview.value &&
    typeof document.status === 'string' &&
    REVIEWABLE_STATUSES.has(document.status as DocumentStatusEnum)
  )
}

async function loadOfferTitles(internshipList: Internship[]) {
  const offerIds = [...new Set(internshipList.map((item) => item.offer))]
  if (!offerIds.length) {
    offerTitles.value = {}
    return
  }
  try {
    const response = await offersApi.list()
    offerTitles.value = Object.fromEntries(
      response.results
        .filter((offer) => offerIds.includes(offer.id))
        .map((offer) => [offer.id, offer.title]),
    )
  } catch {
    offerTitles.value = {}
  }
}

async function loadInternships() {
  const response = await internshipsApi.list()
  internships.value = response.results
  if (!uploadForm.internship && internships.value[0]) {
    uploadForm.internship = internships.value[0].id
  }
  await loadOfferTitles(internships.value)
}

async function loadDocuments() {
  loading.value = true
  error.value = ''
  try {
    const response = await documentsApi.list({
      page: page.value,
      search: search.value || undefined,
      status: statusFilter.value || undefined,
      document_type: typeFilter.value || undefined,
    })
    documents.value = response.results
    total.value = response.count
  } catch {
    error.value = 'Impossible de charger les documents.'
    documents.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

async function submitUpload() {
  if (!selectedFile.value) {
    error.value = 'Veuillez sélectionner un fichier.'
    return
  }
  saving.value = true
  error.value = ''
  try {
    const formData = new FormData()
    formData.append('title', uploadForm.title)
    formData.append('file', selectedFile.value)
    formData.append('document_type', uploadForm.document_type)
    if (uploadForm.internship) formData.append('internship', uploadForm.internship)
    if (uploadForm.comment) formData.append('comment', uploadForm.comment)
    await documentsApi.create(formData)
    resetUploadForm()
    page.value = 1
    await loadDocuments()
  } catch {
    error.value = 'Le document n’a pas pu être déposé.'
  } finally {
    saving.value = false
  }
}

async function reviewDocument(document: Document, action: 'approve' | 'reject') {
  saving.value = true
  error.value = ''
  try {
    await documentsApi.action(document.id, action, {
      comment: reviewComment.value || undefined,
    })
    reviewingId.value = null
    reviewComment.value = ''
    await loadDocuments()
  } catch {
    error.value = 'Le document n’a pas pu être mis à jour.'
  } finally {
    saving.value = false
  }
}

function applyFilters() {
  page.value = 1
  void loadDocuments()
}

function previousPage() {
  if (page.value > 1) page.value -= 1
}

function nextPage() {
  if (page.value < totalPages.value) page.value += 1
}

function formatDate(value?: string | null): string {
  if (!value) return ''
  return new Date(value).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

watch(page, () => {
  void loadDocuments()
})

onMounted(async () => {
  if (canUpload.value) await loadInternships()
  await loadDocuments()
})
</script>

<template>
  <section class="space-y-6">
    <div class="rounded-2xl border border-border bg-white p-6 shadow-sm">
      <h2 class="text-2xl font-semibold tracking-tight">Documents</h2>
      <p class="mt-2 max-w-3xl text-slate-600">
        Déposez vos pièces de stage et suivez leur validation. Les relecteurs
        peuvent approuver ou rejeter les documents en attente.
      </p>
    </div>

    <div
      v-if="canUpload"
      class="rounded-2xl border border-border bg-white p-6 shadow-sm"
    >
      <h3 class="text-lg font-semibold">Déposer un document</h3>
      <p class="mt-1 text-sm text-slate-500">
        Formats acceptés selon la configuration backend (stockage local).
      </p>
      <form class="mt-4 grid gap-4 md:grid-cols-2" @submit.prevent="submitUpload">
        <select
          v-model="uploadForm.internship"
          class="rounded-xl border border-border px-3 py-2.5 text-sm"
        >
          <option value="">Sans stage (ex. CV général)</option>
          <option
            v-for="internship in internships"
            :key="internship.id"
            :value="internship.id"
          >
            {{ internshipLabel(internship, offerTitles) }}
          </option>
        </select>
        <select
          v-model="uploadForm.document_type"
          required
          class="rounded-xl border border-border px-3 py-2.5 text-sm"
        >
          <option value="CV">CV</option>
          <option value="CONVENTION">Convention de stage</option>
          <option value="REPORT">Rapport</option>
        </select>
        <input
          v-model="uploadForm.title"
          required
          class="rounded-xl border border-border px-3 py-2.5 text-sm md:col-span-2"
          placeholder="Titre du document"
        />
        <input
          required
          type="file"
          class="rounded-xl border border-border px-3 py-2.5 text-sm md:col-span-2"
          @change="onFileChange"
        />
        <textarea
          v-model="uploadForm.comment"
          class="min-h-20 rounded-xl border border-border px-3 py-2.5 text-sm md:col-span-2"
          placeholder="Commentaire optionnel"
        />
        <button
          class="inline-flex items-center justify-center rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-60 md:col-span-2"
          :disabled="saving"
        >
          <Loader2 v-if="saving" class="mr-2 h-4 w-4 animate-spin" />
          <Upload v-else class="mr-2 h-4 w-4" />
          Déposer le document
        </button>
      </form>
    </div>

    <div class="rounded-2xl border border-border bg-white p-4">
      <div class="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
        <label class="relative block lg:col-span-2">
          <Search class="absolute left-3 top-3 h-4 w-4 text-slate-400" />
          <input
            v-model="search"
            class="w-full rounded-xl border border-border py-2.5 pl-10 pr-3 text-sm"
            placeholder="Rechercher par titre ou commentaire"
            @keyup.enter="applyFilters"
          />
        </label>
        <select
          v-model="statusFilter"
          class="rounded-xl border border-border px-3 py-2.5 text-sm"
          @change="applyFilters"
        >
          <option value="">Tous les statuts</option>
          <option value="UPLOADED">Déposé</option>
          <option value="IN_REVIEW">En revue</option>
          <option value="APPROVED">Approuvé</option>
          <option value="REJECTED">Rejeté</option>
        </select>
        <select
          v-model="typeFilter"
          class="rounded-xl border border-border px-3 py-2.5 text-sm"
          @change="applyFilters"
        >
          <option value="">Tous les types</option>
          <option value="CV">CV</option>
          <option value="CONVENTION">Convention</option>
          <option value="REPORT">Rapport</option>
        </select>
      </div>
      <div class="mt-3 flex justify-end">
        <button
          class="rounded-xl border border-border px-4 py-2 text-sm font-medium"
          @click="applyFilters"
        >
          Appliquer
        </button>
      </div>
    </div>

    <PageStates
      :loading="loading"
      :error="error && !documents.length ? error : ''"
      :empty="!loading && !error && !documents.length"
      empty-message="Aucun document trouvé pour ces critères."
    >
      <div v-if="error && documents.length" class="mb-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
        {{ error }}
      </div>
      <div class="space-y-3">
        <article
          v-for="document in documents"
          :key="document.id"
          class="rounded-2xl border border-border bg-white p-5 shadow-sm"
        >
          <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div class="min-w-0 flex-1">
              <div class="flex flex-wrap items-center gap-2">
                <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
                  {{ documentTypeLabel(document.document_type) }}
                </span>
                <span
                  class="rounded-full px-3 py-1 text-xs font-medium"
                  :class="documentStatusClass(document.status)"
                >
                  {{ documentStatusLabel(document.status) }}
                </span>
              </div>
              <h3 class="mt-2 text-lg font-semibold">{{ document.title }}</h3>
              <p v-if="document.comment" class="mt-2 text-sm text-slate-600">
                {{ document.comment }}
              </p>
              <p class="mt-2 text-xs text-slate-500">
                Déposé le {{ formatDate(document.created_at) }}
                <span v-if="document.reviewed_at">
                  · Revu le {{ formatDate(document.reviewed_at) }}
                </span>
              </p>
            </div>
            <div class="flex shrink-0 flex-wrap gap-2">
              <a
                v-if="document.file"
                class="inline-flex items-center rounded-xl border border-border px-4 py-2 text-sm font-medium"
                :href="document.file"
                target="_blank"
                rel="noreferrer"
              >
                <Download class="mr-2 h-4 w-4" />
                Télécharger
              </a>
              <template v-if="canReviewDocument(document)">
                <button
                  v-if="reviewingId !== document.id"
                  class="rounded-xl border border-border px-4 py-2 text-sm"
                  @click="reviewingId = document.id"
                >
                  Revoir
                </button>
                <template v-else>
                  <button
                    class="inline-flex items-center rounded-xl border border-emerald-200 px-4 py-2 text-sm text-emerald-700 disabled:opacity-60"
                    :disabled="saving"
                    @click="reviewDocument(document, 'approve')"
                  >
                    <Check class="mr-2 h-4 w-4" />
                    Approuver
                  </button>
                  <button
                    class="inline-flex items-center rounded-xl border border-red-200 px-4 py-2 text-sm text-red-700 disabled:opacity-60"
                    :disabled="saving"
                    @click="reviewDocument(document, 'reject')"
                  >
                    <X class="mr-2 h-4 w-4" />
                    Rejeter
                  </button>
                  <button
                    class="rounded-xl border border-border px-4 py-2 text-sm"
                    @click="reviewingId = null"
                  >
                    Annuler
                  </button>
                </template>
              </template>
            </div>
          </div>
          <div
            v-if="reviewingId === document.id"
            class="mt-4 border-t border-border pt-4"
          >
            <label class="text-sm font-medium text-slate-700">
              Commentaire de relecture (optionnel)
            </label>
            <textarea
              v-model="reviewComment"
              class="mt-2 min-h-20 w-full rounded-xl border border-border px-3 py-2.5 text-sm"
              placeholder="Motif ou remarques pour l’étudiant"
            />
          </div>
        </article>
      </div>
    </PageStates>

    <ListPagination
      :page="page"
      :total-pages="totalPages"
      :total="total"
      :page-size="PAGE_SIZE"
      @previous="previousPage"
      @next="nextPage"
    />
  </section>
</template>
