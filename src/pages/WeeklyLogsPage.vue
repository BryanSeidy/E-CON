<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { Loader2, Pencil, Trash2 } from 'lucide-vue-next'
import { internshipsApi, offersApi, weeklyLogsApi } from '@/api/endpoints'
import ListPagination from '@/components/ui/ListPagination.vue'
import PageStates from '@/components/ui/PageStates.vue'
import { useAuthStore } from '@/stores/auth'
import type { Internship, WeeklyLog } from '@/types/api'
import { internshipLabel } from '@/utils/labels'

const PAGE_SIZE = 20

const auth = useAuthStore()
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const page = ref(1)
const total = ref(0)
const weeklyLogs = ref<WeeklyLog[]>([])
const internships = ref<Internship[]>([])
const offerTitles = ref<Record<string, string>>({})

const createForm = reactive({
  internship: '',
  week_start: '',
  activities: '',
  blockers: '',
  next_steps: '',
})

const editingId = ref<string | null>(null)
const editForm = reactive({
  week_start: '',
  activities: '',
  blockers: '',
  next_steps: '',
})

const canCreate = computed(() => auth.role === 'STUDENT')
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / PAGE_SIZE)))

function canEditLog(log: WeeklyLog): boolean {
  return auth.role === 'STUDENT' && auth.user?.id === log.student
}

function resetCreateForm() {
  Object.assign(createForm, {
    internship: createForm.internship,
    week_start: '',
    activities: '',
    blockers: '',
    next_steps: '',
  })
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
  if (!createForm.internship && internships.value[0]) {
    createForm.internship = internships.value[0].id
  }
  await loadOfferTitles(internships.value)
}

async function loadWeeklyLogs() {
  loading.value = true
  error.value = ''
  try {
    const response = await weeklyLogsApi.list({ page: page.value })
    weeklyLogs.value = response.results
    total.value = response.count
  } catch {
    error.value = 'Impossible de charger les journaux hebdomadaires.'
    weeklyLogs.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

async function submitCreate() {
  saving.value = true
  error.value = ''
  try {
    await weeklyLogsApi.create({ ...createForm })
    resetCreateForm()
    page.value = 1
    await loadWeeklyLogs()
  } catch {
    error.value = 'Le journal hebdomadaire n’a pas pu être enregistré.'
  } finally {
    saving.value = false
  }
}

function startEdit(log: WeeklyLog) {
  editingId.value = log.id
  Object.assign(editForm, {
    week_start: log.week_start,
    activities: log.activities,
    blockers: log.blockers ?? '',
    next_steps: log.next_steps ?? '',
  })
}

function cancelEdit() {
  editingId.value = null
}

async function saveEdit(log: WeeklyLog) {
  saving.value = true
  error.value = ''
  try {
    await weeklyLogsApi.update(log.id, { ...editForm })
    editingId.value = null
    await loadWeeklyLogs()
  } catch {
    error.value = 'Le journal n’a pas pu être mis à jour.'
  } finally {
    saving.value = false
  }
}

async function deleteLog(log: WeeklyLog) {
  if (!window.confirm('Supprimer ce journal hebdomadaire ?')) return
  saving.value = true
  error.value = ''
  try {
    await weeklyLogsApi.remove(log.id)
    if (editingId.value === log.id) editingId.value = null
    await loadWeeklyLogs()
  } catch {
    error.value = 'Le journal n’a pas pu être supprimé.'
  } finally {
    saving.value = false
  }
}

function internshipForLog(log: WeeklyLog): Internship | undefined {
  return internships.value.find((item) => item.id === log.internship)
}

function formatWeekStart(value: string): string {
  return new Date(value).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}

function formatSubmittedAt(value?: string | null): string {
  if (!value) return 'Non soumis'
  return new Date(value).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function previousPage() {
  if (page.value > 1) page.value -= 1
}

function nextPage() {
  if (page.value < totalPages.value) page.value += 1
}

watch(page, () => {
  void loadWeeklyLogs()
})

onMounted(async () => {
  await Promise.all([
    loadInternships(),
    loadWeeklyLogs(),
  ])
})
</script>

<template>
  <section class="space-y-6">
    <div class="rounded-2xl border border-border bg-white p-6 shadow-sm">
      <h2 class="text-2xl font-semibold tracking-tight">Journal hebdomadaire</h2>
      <p class="mt-2 max-w-3xl text-slate-600">
        Consignez vos activités de stage semaine par semaine. Seuls les
        étudiants assignés au stage peuvent créer ou modifier un journal.
      </p>
    </div>

    <div
      v-if="canCreate"
      class="rounded-2xl border border-border bg-white p-6 shadow-sm"
    >
      <h3 class="text-lg font-semibold">Déposer un journal</h3>
      <form class="mt-4 grid gap-4 md:grid-cols-2" @submit.prevent="submitCreate">
        <select
          v-model="createForm.internship"
          required
          class="rounded-xl border border-border px-3 py-2.5 text-sm"
        >
          <option value="" disabled>Sélectionner un stage</option>
          <option
            v-for="internship in internships"
            :key="internship.id"
            :value="internship.id"
          >
            {{ internshipLabel(internship, offerTitles) }}
          </option>
        </select>
        <input
          v-model="createForm.week_start"
          required
          type="date"
          class="rounded-xl border border-border px-3 py-2.5 text-sm"
        />
        <textarea
          v-model="createForm.activities"
          required
          class="min-h-28 rounded-xl border border-border px-3 py-2.5 text-sm md:col-span-2"
          placeholder="Activités réalisées cette semaine"
        />
        <textarea
          v-model="createForm.blockers"
          class="min-h-20 rounded-xl border border-border px-3 py-2.5 text-sm"
          placeholder="Blocages rencontrés"
        />
        <textarea
          v-model="createForm.next_steps"
          class="min-h-20 rounded-xl border border-border px-3 py-2.5 text-sm"
          placeholder="Prochaines étapes"
        />
        <button
          class="inline-flex items-center justify-center rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-60 md:col-span-2"
          :disabled="saving || !internships.length"
        >
          <Loader2 v-if="saving" class="mr-2 h-4 w-4 animate-spin" />
          Enregistrer le journal
        </button>
      </form>
      <p v-if="!internships.length" class="mt-3 text-sm text-amber-700">
        Aucun stage disponible pour déposer un journal.
      </p>
    </div>

    <PageStates
      :loading="loading"
      :error="error && !weeklyLogs.length ? error : ''"
      :empty="!loading && !error && !weeklyLogs.length"
      empty-message="Aucun journal hebdomadaire enregistré."
    >
      <div v-if="error && weeklyLogs.length" class="mb-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
        {{ error }}
      </div>
      <div class="space-y-3">
        <article
          v-for="log in weeklyLogs"
          :key="log.id"
          class="rounded-2xl border border-border bg-white p-5 shadow-sm"
        >
          <div class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
            <div class="min-w-0 flex-1">
              <p class="text-sm text-slate-500">
                {{
                  internshipForLog(log)
                    ? internshipLabel(internshipForLog(log)!, offerTitles)
                    : 'Stage'
                }}
              </p>
              <h3 class="mt-1 text-lg font-semibold">
                Semaine du {{ formatWeekStart(log.week_start) }}
              </h3>
              <p class="mt-1 text-xs text-slate-500">
                Soumis le {{ formatSubmittedAt(log.submitted_at) }}
              </p>
            </div>
            <div v-if="canEditLog(log)" class="flex shrink-0 gap-2">
              <button
                v-if="editingId !== log.id"
                class="inline-flex items-center rounded-xl border border-border px-3 py-2 text-sm"
                @click="startEdit(log)"
              >
                <Pencil class="mr-2 h-4 w-4" />
                Modifier
              </button>
              <button
                class="inline-flex items-center rounded-xl border border-red-200 px-3 py-2 text-sm text-red-700 disabled:opacity-60"
                :disabled="saving"
                @click="deleteLog(log)"
              >
                <Trash2 class="mr-2 h-4 w-4" />
                Supprimer
              </button>
            </div>
          </div>

          <form
            v-if="editingId === log.id"
            class="mt-4 grid gap-4 border-t border-border pt-4 md:grid-cols-2"
            @submit.prevent="saveEdit(log)"
          >
            <input
              v-model="editForm.week_start"
              required
              type="date"
              class="rounded-xl border border-border px-3 py-2.5 text-sm md:col-span-2"
            />
            <textarea
              v-model="editForm.activities"
              required
              class="min-h-28 rounded-xl border border-border px-3 py-2.5 text-sm md:col-span-2"
            />
            <textarea
              v-model="editForm.blockers"
              class="min-h-20 rounded-xl border border-border px-3 py-2.5 text-sm"
              placeholder="Blocages"
            />
            <textarea
              v-model="editForm.next_steps"
              class="min-h-20 rounded-xl border border-border px-3 py-2.5 text-sm"
              placeholder="Prochaines étapes"
            />
            <div class="flex gap-2 md:col-span-2">
              <button
                class="rounded-xl bg-slate-950 px-4 py-2 text-sm font-semibold text-white disabled:opacity-60"
                :disabled="saving"
              >
                Enregistrer
              </button>
              <button
                type="button"
                class="rounded-xl border border-border px-4 py-2 text-sm"
                @click="cancelEdit"
              >
                Annuler
              </button>
            </div>
          </form>

          <template v-else>
            <p class="mt-4 whitespace-pre-line text-sm leading-6 text-slate-700">
              {{ log.activities }}
            </p>
            <p v-if="log.blockers" class="mt-3 text-sm text-red-700">
              <span class="font-medium">Blocages :</span>
              {{ log.blockers }}
            </p>
            <p v-if="log.next_steps" class="mt-2 text-sm text-slate-600">
              <span class="font-medium">Prochaines étapes :</span>
              {{ log.next_steps }}
            </p>
          </template>
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
