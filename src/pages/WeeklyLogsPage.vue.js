import { computed, onMounted, reactive, ref, watch } from 'vue';
import { Loader2, Pencil, Trash2 } from 'lucide-vue-next';
import { internshipsApi, offersApi, weeklyLogsApi } from '@/api/endpoints';
import ListPagination from '@/components/ui/ListPagination.vue';
import PageStates from '@/components/ui/PageStates.vue';
import { useAuthStore } from '@/stores/auth';
import { internshipLabel } from '@/utils/labels';
const PAGE_SIZE = 20;
const auth = useAuthStore();
const loading = ref(true);
const saving = ref(false);
const error = ref('');
const page = ref(1);
const total = ref(0);
const weeklyLogs = ref([]);
const internships = ref([]);
const offerTitles = ref({});
const createForm = reactive({
    internship: '',
    week_start: '',
    activities: '',
    blockers: '',
    next_steps: '',
});
const editingId = ref(null);
const editForm = reactive({
    week_start: '',
    activities: '',
    blockers: '',
    next_steps: '',
});
const canCreate = computed(() => auth.role === 'STUDENT');
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / PAGE_SIZE)));
function canEditLog(log) {
    return auth.role === 'STUDENT' && auth.user?.id === log.student;
}
function resetCreateForm() {
    Object.assign(createForm, {
        internship: createForm.internship,
        week_start: '',
        activities: '',
        blockers: '',
        next_steps: '',
    });
}
async function loadOfferTitles(internshipList) {
    const offerIds = [...new Set(internshipList.map((item) => item.offer))];
    if (!offerIds.length) {
        offerTitles.value = {};
        return;
    }
    try {
        const response = await offersApi.list();
        offerTitles.value = Object.fromEntries(response.results
            .filter((offer) => offerIds.includes(offer.id))
            .map((offer) => [offer.id, offer.title]));
    }
    catch {
        offerTitles.value = {};
    }
}
async function loadInternships() {
    const response = await internshipsApi.list();
    internships.value = response.results;
    if (!createForm.internship && internships.value[0]) {
        createForm.internship = internships.value[0].id;
    }
    await loadOfferTitles(internships.value);
}
async function loadWeeklyLogs() {
    loading.value = true;
    error.value = '';
    try {
        const response = await weeklyLogsApi.list({ page: page.value });
        weeklyLogs.value = response.results;
        total.value = response.count;
    }
    catch {
        error.value = 'Impossible de charger les journaux hebdomadaires.';
        weeklyLogs.value = [];
        total.value = 0;
    }
    finally {
        loading.value = false;
    }
}
async function submitCreate() {
    saving.value = true;
    error.value = '';
    try {
        await weeklyLogsApi.create({ ...createForm });
        resetCreateForm();
        page.value = 1;
        await loadWeeklyLogs();
    }
    catch {
        error.value = 'Le journal hebdomadaire n’a pas pu être enregistré.';
    }
    finally {
        saving.value = false;
    }
}
function startEdit(log) {
    editingId.value = log.id;
    Object.assign(editForm, {
        week_start: log.week_start,
        activities: log.activities,
        blockers: log.blockers ?? '',
        next_steps: log.next_steps ?? '',
    });
}
function cancelEdit() {
    editingId.value = null;
}
async function saveEdit(log) {
    saving.value = true;
    error.value = '';
    try {
        await weeklyLogsApi.update(log.id, { ...editForm });
        editingId.value = null;
        await loadWeeklyLogs();
    }
    catch {
        error.value = 'Le journal n’a pas pu être mis à jour.';
    }
    finally {
        saving.value = false;
    }
}
async function deleteLog(log) {
    if (!window.confirm('Supprimer ce journal hebdomadaire ?'))
        return;
    saving.value = true;
    error.value = '';
    try {
        await weeklyLogsApi.remove(log.id);
        if (editingId.value === log.id)
            editingId.value = null;
        await loadWeeklyLogs();
    }
    catch {
        error.value = 'Le journal n’a pas pu être supprimé.';
    }
    finally {
        saving.value = false;
    }
}
function internshipForLog(log) {
    return internships.value.find((item) => item.id === log.internship);
}
function formatWeekStart(value) {
    return new Date(value).toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
    });
}
function formatSubmittedAt(value) {
    if (!value)
        return 'Non soumis';
    return new Date(value).toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}
function previousPage() {
    if (page.value > 1)
        page.value -= 1;
}
function nextPage() {
    if (page.value < totalPages.value)
        page.value += 1;
}
watch(page, () => {
    void loadWeeklyLogs();
});
onMounted(async () => {
    await Promise.all([
        loadInternships(),
        loadWeeklyLogs(),
    ]);
});
const __VLS_ctx = {
    ...{},
    ...{},
};
let __VLS_components;
let __VLS_intrinsics;
let __VLS_directives;
__VLS_asFunctionalElement1(__VLS_intrinsics.section, __VLS_intrinsics.section)({
    ...{ class: "space-y-6" },
});
/** @type {__VLS_StyleScopedClasses['space-y-6']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "rounded-2xl border border-border bg-white p-6 shadow-sm" },
});
/** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
/** @type {__VLS_StyleScopedClasses['border']} */ ;
/** @type {__VLS_StyleScopedClasses['border-border']} */ ;
/** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
/** @type {__VLS_StyleScopedClasses['p-6']} */ ;
/** @type {__VLS_StyleScopedClasses['shadow-sm']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.h2, __VLS_intrinsics.h2)({
    ...{ class: "text-2xl font-semibold tracking-tight" },
});
/** @type {__VLS_StyleScopedClasses['text-2xl']} */ ;
/** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
/** @type {__VLS_StyleScopedClasses['tracking-tight']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
    ...{ class: "mt-2 max-w-3xl text-slate-600" },
});
/** @type {__VLS_StyleScopedClasses['mt-2']} */ ;
/** @type {__VLS_StyleScopedClasses['max-w-3xl']} */ ;
/** @type {__VLS_StyleScopedClasses['text-slate-600']} */ ;
if (__VLS_ctx.canCreate) {
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "rounded-2xl border border-border bg-white p-6 shadow-sm" },
    });
    /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
    /** @type {__VLS_StyleScopedClasses['border']} */ ;
    /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
    /** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
    /** @type {__VLS_StyleScopedClasses['p-6']} */ ;
    /** @type {__VLS_StyleScopedClasses['shadow-sm']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.h3, __VLS_intrinsics.h3)({
        ...{ class: "text-lg font-semibold" },
    });
    /** @type {__VLS_StyleScopedClasses['text-lg']} */ ;
    /** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.form, __VLS_intrinsics.form)({
        ...{ onSubmit: (__VLS_ctx.submitCreate) },
        ...{ class: "mt-4 grid gap-4 md:grid-cols-2" },
    });
    /** @type {__VLS_StyleScopedClasses['mt-4']} */ ;
    /** @type {__VLS_StyleScopedClasses['grid']} */ ;
    /** @type {__VLS_StyleScopedClasses['gap-4']} */ ;
    /** @type {__VLS_StyleScopedClasses['md:grid-cols-2']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.select, __VLS_intrinsics.select)({
        value: (__VLS_ctx.createForm.internship),
        required: true,
        ...{ class: "rounded-xl border border-border px-3 py-2.5 text-sm" },
    });
    /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
    /** @type {__VLS_StyleScopedClasses['border']} */ ;
    /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
    /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
    /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.option, __VLS_intrinsics.option)({
        value: "",
        disabled: true,
    });
    for (const [internship] of __VLS_vFor((__VLS_ctx.internships))) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.option, __VLS_intrinsics.option)({
            key: (internship.id),
            value: (internship.id),
        });
        (__VLS_ctx.internshipLabel(internship, __VLS_ctx.offerTitles));
        // @ts-ignore
        [canCreate, submitCreate, createForm, internships, internshipLabel, offerTitles,];
    }
    __VLS_asFunctionalElement1(__VLS_intrinsics.input)({
        required: true,
        type: "date",
        ...{ class: "rounded-xl border border-border px-3 py-2.5 text-sm" },
    });
    (__VLS_ctx.createForm.week_start);
    /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
    /** @type {__VLS_StyleScopedClasses['border']} */ ;
    /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
    /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
    /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.textarea)({
        value: (__VLS_ctx.createForm.activities),
        required: true,
        ...{ class: "min-h-28 rounded-xl border border-border px-3 py-2.5 text-sm md:col-span-2" },
        placeholder: "Activités réalisées cette semaine",
    });
    /** @type {__VLS_StyleScopedClasses['min-h-28']} */ ;
    /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
    /** @type {__VLS_StyleScopedClasses['border']} */ ;
    /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
    /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
    /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    /** @type {__VLS_StyleScopedClasses['md:col-span-2']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.textarea)({
        value: (__VLS_ctx.createForm.blockers),
        ...{ class: "min-h-20 rounded-xl border border-border px-3 py-2.5 text-sm" },
        placeholder: "Blocages rencontrés",
    });
    /** @type {__VLS_StyleScopedClasses['min-h-20']} */ ;
    /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
    /** @type {__VLS_StyleScopedClasses['border']} */ ;
    /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
    /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
    /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.textarea)({
        value: (__VLS_ctx.createForm.next_steps),
        ...{ class: "min-h-20 rounded-xl border border-border px-3 py-2.5 text-sm" },
        placeholder: "Prochaines étapes",
    });
    /** @type {__VLS_StyleScopedClasses['min-h-20']} */ ;
    /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
    /** @type {__VLS_StyleScopedClasses['border']} */ ;
    /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
    /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
    /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
        ...{ class: "inline-flex items-center justify-center rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-60 md:col-span-2" },
        disabled: (__VLS_ctx.saving || !__VLS_ctx.internships.length),
    });
    /** @type {__VLS_StyleScopedClasses['inline-flex']} */ ;
    /** @type {__VLS_StyleScopedClasses['items-center']} */ ;
    /** @type {__VLS_StyleScopedClasses['justify-center']} */ ;
    /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
    /** @type {__VLS_StyleScopedClasses['bg-slate-950']} */ ;
    /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
    /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    /** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-white']} */ ;
    /** @type {__VLS_StyleScopedClasses['disabled:opacity-60']} */ ;
    /** @type {__VLS_StyleScopedClasses['md:col-span-2']} */ ;
    if (__VLS_ctx.saving) {
        let __VLS_0;
        /** @ts-ignore @type { | typeof __VLS_components.Loader2} */
        Loader2;
        // @ts-ignore
        const __VLS_1 = __VLS_asFunctionalComponent1(__VLS_0, new __VLS_0({
            ...{ class: "mr-2 h-4 w-4 animate-spin" },
        }));
        const __VLS_2 = __VLS_1({
            ...{ class: "mr-2 h-4 w-4 animate-spin" },
        }, ...__VLS_functionalComponentArgsRest(__VLS_1));
        /** @type {__VLS_StyleScopedClasses['mr-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['animate-spin']} */ ;
    }
    if (!__VLS_ctx.internships.length) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
            ...{ class: "mt-3 text-sm text-amber-700" },
        });
        /** @type {__VLS_StyleScopedClasses['mt-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-amber-700']} */ ;
    }
}
const __VLS_5 = PageStates || PageStates;
// @ts-ignore
const __VLS_6 = __VLS_asFunctionalComponent1(__VLS_5, new __VLS_5({
    loading: (__VLS_ctx.loading),
    error: (__VLS_ctx.error && !__VLS_ctx.weeklyLogs.length ? __VLS_ctx.error : ''),
    empty: (!__VLS_ctx.loading && !__VLS_ctx.error && !__VLS_ctx.weeklyLogs.length),
    emptyMessage: "Aucun journal hebdomadaire enregistré.",
}));
const __VLS_7 = __VLS_6({
    loading: (__VLS_ctx.loading),
    error: (__VLS_ctx.error && !__VLS_ctx.weeklyLogs.length ? __VLS_ctx.error : ''),
    empty: (!__VLS_ctx.loading && !__VLS_ctx.error && !__VLS_ctx.weeklyLogs.length),
    emptyMessage: "Aucun journal hebdomadaire enregistré.",
}, ...__VLS_functionalComponentArgsRest(__VLS_6));
const { default: __VLS_10 } = __VLS_8.slots;
if (__VLS_ctx.error && __VLS_ctx.weeklyLogs.length) {
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "mb-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700" },
    });
    /** @type {__VLS_StyleScopedClasses['mb-4']} */ ;
    /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
    /** @type {__VLS_StyleScopedClasses['border']} */ ;
    /** @type {__VLS_StyleScopedClasses['border-red-200']} */ ;
    /** @type {__VLS_StyleScopedClasses['bg-red-50']} */ ;
    /** @type {__VLS_StyleScopedClasses['p-4']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-red-700']} */ ;
    (__VLS_ctx.error);
}
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "space-y-3" },
});
/** @type {__VLS_StyleScopedClasses['space-y-3']} */ ;
for (const [log] of __VLS_vFor((__VLS_ctx.weeklyLogs))) {
    __VLS_asFunctionalElement1(__VLS_intrinsics.article, __VLS_intrinsics.article)({
        key: (log.id),
        ...{ class: "rounded-2xl border border-border bg-white p-5 shadow-sm" },
    });
    /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
    /** @type {__VLS_StyleScopedClasses['border']} */ ;
    /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
    /** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
    /** @type {__VLS_StyleScopedClasses['p-5']} */ ;
    /** @type {__VLS_StyleScopedClasses['shadow-sm']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "flex flex-col gap-4 md:flex-row md:items-start md:justify-between" },
    });
    /** @type {__VLS_StyleScopedClasses['flex']} */ ;
    /** @type {__VLS_StyleScopedClasses['flex-col']} */ ;
    /** @type {__VLS_StyleScopedClasses['gap-4']} */ ;
    /** @type {__VLS_StyleScopedClasses['md:flex-row']} */ ;
    /** @type {__VLS_StyleScopedClasses['md:items-start']} */ ;
    /** @type {__VLS_StyleScopedClasses['md:justify-between']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "min-w-0 flex-1" },
    });
    /** @type {__VLS_StyleScopedClasses['min-w-0']} */ ;
    /** @type {__VLS_StyleScopedClasses['flex-1']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
        ...{ class: "text-sm text-slate-500" },
    });
    /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-slate-500']} */ ;
    (__VLS_ctx.internshipForLog(log)
        ? __VLS_ctx.internshipLabel(__VLS_ctx.internshipForLog(log), __VLS_ctx.offerTitles)
        : 'Stage');
    __VLS_asFunctionalElement1(__VLS_intrinsics.h3, __VLS_intrinsics.h3)({
        ...{ class: "mt-1 text-lg font-semibold" },
    });
    /** @type {__VLS_StyleScopedClasses['mt-1']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-lg']} */ ;
    /** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
    (__VLS_ctx.formatWeekStart(log.week_start));
    __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
        ...{ class: "mt-1 text-xs text-slate-500" },
    });
    /** @type {__VLS_StyleScopedClasses['mt-1']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-xs']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-slate-500']} */ ;
    (__VLS_ctx.formatSubmittedAt(log.submitted_at));
    if (__VLS_ctx.canEditLog(log)) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "flex shrink-0 gap-2" },
        });
        /** @type {__VLS_StyleScopedClasses['flex']} */ ;
        /** @type {__VLS_StyleScopedClasses['shrink-0']} */ ;
        /** @type {__VLS_StyleScopedClasses['gap-2']} */ ;
        if (__VLS_ctx.editingId !== log.id) {
            __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
                ...{ onClick: (...[$event]) => {
                        if (!(__VLS_ctx.canEditLog(log)))
                            return;
                        if (!(__VLS_ctx.editingId !== log.id))
                            return;
                        __VLS_ctx.startEdit(log);
                        // @ts-ignore
                        [createForm, createForm, createForm, createForm, internships, internships, internshipLabel, offerTitles, saving, saving, loading, loading, error, error, error, error, error, weeklyLogs, weeklyLogs, weeklyLogs, weeklyLogs, internshipForLog, internshipForLog, formatWeekStart, formatSubmittedAt, canEditLog, editingId, startEdit,];
                    } },
                ...{ class: "inline-flex items-center rounded-xl border border-border px-3 py-2 text-sm" },
            });
            /** @type {__VLS_StyleScopedClasses['inline-flex']} */ ;
            /** @type {__VLS_StyleScopedClasses['items-center']} */ ;
            /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['border']} */ ;
            /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
            /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
            /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
            let __VLS_11;
            /** @ts-ignore @type { | typeof __VLS_components.Pencil} */
            Pencil;
            // @ts-ignore
            const __VLS_12 = __VLS_asFunctionalComponent1(__VLS_11, new __VLS_11({
                ...{ class: "mr-2 h-4 w-4" },
            }));
            const __VLS_13 = __VLS_12({
                ...{ class: "mr-2 h-4 w-4" },
            }, ...__VLS_functionalComponentArgsRest(__VLS_12));
            /** @type {__VLS_StyleScopedClasses['mr-2']} */ ;
            /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
        }
        __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
            ...{ onClick: (...[$event]) => {
                    if (!(__VLS_ctx.canEditLog(log)))
                        return;
                    __VLS_ctx.deleteLog(log);
                    // @ts-ignore
                    [deleteLog,];
                } },
            ...{ class: "inline-flex items-center rounded-xl border border-red-200 px-3 py-2 text-sm text-red-700 disabled:opacity-60" },
            disabled: (__VLS_ctx.saving),
        });
        /** @type {__VLS_StyleScopedClasses['inline-flex']} */ ;
        /** @type {__VLS_StyleScopedClasses['items-center']} */ ;
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-red-200']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-red-700']} */ ;
        /** @type {__VLS_StyleScopedClasses['disabled:opacity-60']} */ ;
        let __VLS_16;
        /** @ts-ignore @type { | typeof __VLS_components.Trash2} */
        Trash2;
        // @ts-ignore
        const __VLS_17 = __VLS_asFunctionalComponent1(__VLS_16, new __VLS_16({
            ...{ class: "mr-2 h-4 w-4" },
        }));
        const __VLS_18 = __VLS_17({
            ...{ class: "mr-2 h-4 w-4" },
        }, ...__VLS_functionalComponentArgsRest(__VLS_17));
        /** @type {__VLS_StyleScopedClasses['mr-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
    }
    if (__VLS_ctx.editingId === log.id) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.form, __VLS_intrinsics.form)({
            ...{ onSubmit: (...[$event]) => {
                    if (!(__VLS_ctx.editingId === log.id))
                        return;
                    __VLS_ctx.saveEdit(log);
                    // @ts-ignore
                    [saving, editingId, saveEdit,];
                } },
            ...{ class: "mt-4 grid gap-4 border-t border-border pt-4 md:grid-cols-2" },
        });
        /** @type {__VLS_StyleScopedClasses['mt-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['grid']} */ ;
        /** @type {__VLS_StyleScopedClasses['gap-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-t']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['pt-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['md:grid-cols-2']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.input)({
            required: true,
            type: "date",
            ...{ class: "rounded-xl border border-border px-3 py-2.5 text-sm md:col-span-2" },
        });
        (__VLS_ctx.editForm.week_start);
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['md:col-span-2']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.textarea)({
            value: (__VLS_ctx.editForm.activities),
            required: true,
            ...{ class: "min-h-28 rounded-xl border border-border px-3 py-2.5 text-sm md:col-span-2" },
        });
        /** @type {__VLS_StyleScopedClasses['min-h-28']} */ ;
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['md:col-span-2']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.textarea)({
            value: (__VLS_ctx.editForm.blockers),
            ...{ class: "min-h-20 rounded-xl border border-border px-3 py-2.5 text-sm" },
            placeholder: "Blocages",
        });
        /** @type {__VLS_StyleScopedClasses['min-h-20']} */ ;
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.textarea)({
            value: (__VLS_ctx.editForm.next_steps),
            ...{ class: "min-h-20 rounded-xl border border-border px-3 py-2.5 text-sm" },
            placeholder: "Prochaines étapes",
        });
        /** @type {__VLS_StyleScopedClasses['min-h-20']} */ ;
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "flex gap-2 md:col-span-2" },
        });
        /** @type {__VLS_StyleScopedClasses['flex']} */ ;
        /** @type {__VLS_StyleScopedClasses['gap-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['md:col-span-2']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
            ...{ class: "rounded-xl bg-slate-950 px-4 py-2 text-sm font-semibold text-white disabled:opacity-60" },
            disabled: (__VLS_ctx.saving),
        });
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['bg-slate-950']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-white']} */ ;
        /** @type {__VLS_StyleScopedClasses['disabled:opacity-60']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
            ...{ onClick: (__VLS_ctx.cancelEdit) },
            type: "button",
            ...{ class: "rounded-xl border border-border px-4 py-2 text-sm" },
        });
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    }
    else {
        __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
            ...{ class: "mt-4 whitespace-pre-line text-sm leading-6 text-slate-700" },
        });
        /** @type {__VLS_StyleScopedClasses['mt-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['whitespace-pre-line']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['leading-6']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-slate-700']} */ ;
        (log.activities);
        if (log.blockers) {
            __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
                ...{ class: "mt-3 text-sm text-red-700" },
            });
            /** @type {__VLS_StyleScopedClasses['mt-3']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-red-700']} */ ;
            __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
                ...{ class: "font-medium" },
            });
            /** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
            (log.blockers);
        }
        if (log.next_steps) {
            __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
                ...{ class: "mt-2 text-sm text-slate-600" },
            });
            /** @type {__VLS_StyleScopedClasses['mt-2']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-slate-600']} */ ;
            __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
                ...{ class: "font-medium" },
            });
            /** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
            (log.next_steps);
        }
    }
    // @ts-ignore
    [saving, editForm, editForm, editForm, editForm, cancelEdit,];
}
// @ts-ignore
[];
var __VLS_8;
const __VLS_21 = ListPagination;
// @ts-ignore
const __VLS_22 = __VLS_asFunctionalComponent1(__VLS_21, new __VLS_21({
    ...{ 'onPrevious': {} },
    ...{ 'onNext': {} },
    page: (__VLS_ctx.page),
    totalPages: (__VLS_ctx.totalPages),
    total: (__VLS_ctx.total),
    pageSize: (__VLS_ctx.PAGE_SIZE),
}));
const __VLS_23 = __VLS_22({
    ...{ 'onPrevious': {} },
    ...{ 'onNext': {} },
    page: (__VLS_ctx.page),
    totalPages: (__VLS_ctx.totalPages),
    total: (__VLS_ctx.total),
    pageSize: (__VLS_ctx.PAGE_SIZE),
}, ...__VLS_functionalComponentArgsRest(__VLS_22));
let __VLS_26;
const __VLS_27 = {
    /** @type {typeof __VLS_26.previous} */
    onPrevious: (__VLS_ctx.previousPage),
};
const __VLS_28 = {
    /** @type {typeof __VLS_26.next} */
    onNext: (__VLS_ctx.nextPage),
};
var __VLS_24;
var __VLS_25;
// @ts-ignore
[page, totalPages, total, PAGE_SIZE, previousPage, nextPage,];
const __VLS_export = (await import('vue')).defineComponent({});
export default {};
//# sourceMappingURL=WeeklyLogsPage.vue.js.map