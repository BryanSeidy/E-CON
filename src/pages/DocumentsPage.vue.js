import { computed, onMounted, reactive, ref, watch } from 'vue';
import { Check, Download, Loader2, Search, Upload, X, } from 'lucide-vue-next';
import { documentsApi, internshipsApi, offersApi } from '@/api/endpoints';
import ListPagination from '@/components/ui/ListPagination.vue';
import PageStates from '@/components/ui/PageStates.vue';
import { useAuthStore } from '@/stores/auth';
import { documentStatusClass, documentStatusLabel, documentTypeLabel, internshipLabel, } from '@/utils/labels';
const PAGE_SIZE = 20;
const REVIEWER_ROLES = new Set([
    'COMPANY_MEMBER',
    'ACADEMIC_SUPERVISOR',
    'HEAD_OF_PROGRAM',
    'UNIVERSITY_ADMIN',
    'SUPER_ADMIN',
]);
const REVIEWABLE_STATUSES = new Set(['UPLOADED', 'IN_REVIEW']);
const auth = useAuthStore();
const loading = ref(true);
const saving = ref(false);
const error = ref('');
const search = ref('');
const statusFilter = ref('');
const typeFilter = ref('');
const page = ref(1);
const total = ref(0);
const documents = ref([]);
const internships = ref([]);
const offerTitles = ref({});
const uploadForm = reactive({
    internship: '',
    document_type: 'CV',
    title: '',
    comment: '',
});
const selectedFile = ref(null);
const reviewComment = ref('');
const reviewingId = ref(null);
const canUpload = computed(() => auth.role === 'STUDENT');
const canReview = computed(() => REVIEWER_ROLES.has(auth.role ?? ''));
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / PAGE_SIZE)));
function resetUploadForm() {
    Object.assign(uploadForm, {
        internship: uploadForm.internship,
        document_type: 'CV',
        title: '',
        comment: '',
    });
    selectedFile.value = null;
}
function onFileChange(event) {
    const input = event.target;
    selectedFile.value = input.files?.[0] ?? null;
}
function canReviewDocument(document) {
    return (canReview.value &&
        typeof document.status === 'string' &&
        REVIEWABLE_STATUSES.has(document.status));
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
    if (!uploadForm.internship && internships.value[0]) {
        uploadForm.internship = internships.value[0].id;
    }
    await loadOfferTitles(internships.value);
}
async function loadDocuments() {
    loading.value = true;
    error.value = '';
    try {
        const response = await documentsApi.list({
            page: page.value,
            search: search.value || undefined,
            status: statusFilter.value || undefined,
            document_type: typeFilter.value || undefined,
        });
        documents.value = response.results;
        total.value = response.count;
    }
    catch {
        error.value = 'Impossible de charger les documents.';
        documents.value = [];
        total.value = 0;
    }
    finally {
        loading.value = false;
    }
}
async function submitUpload() {
    if (!selectedFile.value) {
        error.value = 'Veuillez sélectionner un fichier.';
        return;
    }
    saving.value = true;
    error.value = '';
    try {
        const formData = new FormData();
        formData.append('title', uploadForm.title);
        formData.append('file', selectedFile.value);
        formData.append('document_type', uploadForm.document_type);
        if (uploadForm.internship)
            formData.append('internship', uploadForm.internship);
        if (uploadForm.comment)
            formData.append('comment', uploadForm.comment);
        await documentsApi.create(formData);
        resetUploadForm();
        page.value = 1;
        await loadDocuments();
    }
    catch {
        error.value = 'Le document n’a pas pu être déposé.';
    }
    finally {
        saving.value = false;
    }
}
async function reviewDocument(document, action) {
    saving.value = true;
    error.value = '';
    try {
        await documentsApi.action(document.id, action, {
            comment: reviewComment.value || undefined,
        });
        reviewingId.value = null;
        reviewComment.value = '';
        await loadDocuments();
    }
    catch {
        error.value = 'Le document n’a pas pu être mis à jour.';
    }
    finally {
        saving.value = false;
    }
}
function applyFilters() {
    page.value = 1;
    void loadDocuments();
}
function previousPage() {
    if (page.value > 1)
        page.value -= 1;
}
function nextPage() {
    if (page.value < totalPages.value)
        page.value += 1;
}
function formatDate(value) {
    if (!value)
        return '';
    return new Date(value).toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
    });
}
watch(page, () => {
    void loadDocuments();
});
onMounted(async () => {
    if (canUpload.value)
        await loadInternships();
    await loadDocuments();
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
if (__VLS_ctx.canUpload) {
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
    __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
        ...{ class: "mt-1 text-sm text-slate-500" },
    });
    /** @type {__VLS_StyleScopedClasses['mt-1']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-slate-500']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.form, __VLS_intrinsics.form)({
        ...{ onSubmit: (__VLS_ctx.submitUpload) },
        ...{ class: "mt-4 grid gap-4 md:grid-cols-2" },
    });
    /** @type {__VLS_StyleScopedClasses['mt-4']} */ ;
    /** @type {__VLS_StyleScopedClasses['grid']} */ ;
    /** @type {__VLS_StyleScopedClasses['gap-4']} */ ;
    /** @type {__VLS_StyleScopedClasses['md:grid-cols-2']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.select, __VLS_intrinsics.select)({
        value: (__VLS_ctx.uploadForm.internship),
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
    });
    for (const [internship] of __VLS_vFor((__VLS_ctx.internships))) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.option, __VLS_intrinsics.option)({
            key: (internship.id),
            value: (internship.id),
        });
        (__VLS_ctx.internshipLabel(internship, __VLS_ctx.offerTitles));
        // @ts-ignore
        [canUpload, submitUpload, uploadForm, internships, internshipLabel, offerTitles,];
    }
    __VLS_asFunctionalElement1(__VLS_intrinsics.select, __VLS_intrinsics.select)({
        value: (__VLS_ctx.uploadForm.document_type),
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
        value: "CV",
    });
    __VLS_asFunctionalElement1(__VLS_intrinsics.option, __VLS_intrinsics.option)({
        value: "CONVENTION",
    });
    __VLS_asFunctionalElement1(__VLS_intrinsics.option, __VLS_intrinsics.option)({
        value: "REPORT",
    });
    __VLS_asFunctionalElement1(__VLS_intrinsics.input)({
        required: true,
        ...{ class: "rounded-xl border border-border px-3 py-2.5 text-sm md:col-span-2" },
        placeholder: "Titre du document",
    });
    (__VLS_ctx.uploadForm.title);
    /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
    /** @type {__VLS_StyleScopedClasses['border']} */ ;
    /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
    /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
    /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    /** @type {__VLS_StyleScopedClasses['md:col-span-2']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.input)({
        ...{ onChange: (__VLS_ctx.onFileChange) },
        required: true,
        type: "file",
        ...{ class: "rounded-xl border border-border px-3 py-2.5 text-sm md:col-span-2" },
    });
    /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
    /** @type {__VLS_StyleScopedClasses['border']} */ ;
    /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
    /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
    /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    /** @type {__VLS_StyleScopedClasses['md:col-span-2']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.textarea)({
        value: (__VLS_ctx.uploadForm.comment),
        ...{ class: "min-h-20 rounded-xl border border-border px-3 py-2.5 text-sm md:col-span-2" },
        placeholder: "Commentaire optionnel",
    });
    /** @type {__VLS_StyleScopedClasses['min-h-20']} */ ;
    /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
    /** @type {__VLS_StyleScopedClasses['border']} */ ;
    /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
    /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
    /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    /** @type {__VLS_StyleScopedClasses['md:col-span-2']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
        ...{ class: "inline-flex items-center justify-center rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-60 md:col-span-2" },
        disabled: (__VLS_ctx.saving),
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
    else {
        let __VLS_5;
        /** @ts-ignore @type { | typeof __VLS_components.Upload} */
        Upload;
        // @ts-ignore
        const __VLS_6 = __VLS_asFunctionalComponent1(__VLS_5, new __VLS_5({
            ...{ class: "mr-2 h-4 w-4" },
        }));
        const __VLS_7 = __VLS_6({
            ...{ class: "mr-2 h-4 w-4" },
        }, ...__VLS_functionalComponentArgsRest(__VLS_6));
        /** @type {__VLS_StyleScopedClasses['mr-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
    }
}
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "rounded-2xl border border-border bg-white p-4" },
});
/** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
/** @type {__VLS_StyleScopedClasses['border']} */ ;
/** @type {__VLS_StyleScopedClasses['border-border']} */ ;
/** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
/** @type {__VLS_StyleScopedClasses['p-4']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "grid gap-3 md:grid-cols-2 lg:grid-cols-4" },
});
/** @type {__VLS_StyleScopedClasses['grid']} */ ;
/** @type {__VLS_StyleScopedClasses['gap-3']} */ ;
/** @type {__VLS_StyleScopedClasses['md:grid-cols-2']} */ ;
/** @type {__VLS_StyleScopedClasses['lg:grid-cols-4']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.label, __VLS_intrinsics.label)({
    ...{ class: "relative block lg:col-span-2" },
});
/** @type {__VLS_StyleScopedClasses['relative']} */ ;
/** @type {__VLS_StyleScopedClasses['block']} */ ;
/** @type {__VLS_StyleScopedClasses['lg:col-span-2']} */ ;
let __VLS_10;
/** @ts-ignore @type { | typeof __VLS_components.Search} */
Search;
// @ts-ignore
const __VLS_11 = __VLS_asFunctionalComponent1(__VLS_10, new __VLS_10({
    ...{ class: "absolute left-3 top-3 h-4 w-4 text-slate-400" },
}));
const __VLS_12 = __VLS_11({
    ...{ class: "absolute left-3 top-3 h-4 w-4 text-slate-400" },
}, ...__VLS_functionalComponentArgsRest(__VLS_11));
/** @type {__VLS_StyleScopedClasses['absolute']} */ ;
/** @type {__VLS_StyleScopedClasses['left-3']} */ ;
/** @type {__VLS_StyleScopedClasses['top-3']} */ ;
/** @type {__VLS_StyleScopedClasses['h-4']} */ ;
/** @type {__VLS_StyleScopedClasses['w-4']} */ ;
/** @type {__VLS_StyleScopedClasses['text-slate-400']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.input)({
    ...{ onKeyup: (__VLS_ctx.applyFilters) },
    ...{ class: "w-full rounded-xl border border-border py-2.5 pl-10 pr-3 text-sm" },
    placeholder: "Rechercher par titre ou commentaire",
});
(__VLS_ctx.search);
/** @type {__VLS_StyleScopedClasses['w-full']} */ ;
/** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
/** @type {__VLS_StyleScopedClasses['border']} */ ;
/** @type {__VLS_StyleScopedClasses['border-border']} */ ;
/** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
/** @type {__VLS_StyleScopedClasses['pl-10']} */ ;
/** @type {__VLS_StyleScopedClasses['pr-3']} */ ;
/** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.select, __VLS_intrinsics.select)({
    ...{ onChange: (__VLS_ctx.applyFilters) },
    value: (__VLS_ctx.statusFilter),
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
});
__VLS_asFunctionalElement1(__VLS_intrinsics.option, __VLS_intrinsics.option)({
    value: "UPLOADED",
});
__VLS_asFunctionalElement1(__VLS_intrinsics.option, __VLS_intrinsics.option)({
    value: "IN_REVIEW",
});
__VLS_asFunctionalElement1(__VLS_intrinsics.option, __VLS_intrinsics.option)({
    value: "APPROVED",
});
__VLS_asFunctionalElement1(__VLS_intrinsics.option, __VLS_intrinsics.option)({
    value: "REJECTED",
});
__VLS_asFunctionalElement1(__VLS_intrinsics.select, __VLS_intrinsics.select)({
    ...{ onChange: (__VLS_ctx.applyFilters) },
    value: (__VLS_ctx.typeFilter),
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
});
__VLS_asFunctionalElement1(__VLS_intrinsics.option, __VLS_intrinsics.option)({
    value: "CV",
});
__VLS_asFunctionalElement1(__VLS_intrinsics.option, __VLS_intrinsics.option)({
    value: "CONVENTION",
});
__VLS_asFunctionalElement1(__VLS_intrinsics.option, __VLS_intrinsics.option)({
    value: "REPORT",
});
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "mt-3 flex justify-end" },
});
/** @type {__VLS_StyleScopedClasses['mt-3']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['justify-end']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
    ...{ onClick: (__VLS_ctx.applyFilters) },
    ...{ class: "rounded-xl border border-border px-4 py-2 text-sm font-medium" },
});
/** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
/** @type {__VLS_StyleScopedClasses['border']} */ ;
/** @type {__VLS_StyleScopedClasses['border-border']} */ ;
/** @type {__VLS_StyleScopedClasses['px-4']} */ ;
/** @type {__VLS_StyleScopedClasses['py-2']} */ ;
/** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
/** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
const __VLS_15 = PageStates || PageStates;
// @ts-ignore
const __VLS_16 = __VLS_asFunctionalComponent1(__VLS_15, new __VLS_15({
    loading: (__VLS_ctx.loading),
    error: (__VLS_ctx.error && !__VLS_ctx.documents.length ? __VLS_ctx.error : ''),
    empty: (!__VLS_ctx.loading && !__VLS_ctx.error && !__VLS_ctx.documents.length),
    emptyMessage: "Aucun document trouvé pour ces critères.",
}));
const __VLS_17 = __VLS_16({
    loading: (__VLS_ctx.loading),
    error: (__VLS_ctx.error && !__VLS_ctx.documents.length ? __VLS_ctx.error : ''),
    empty: (!__VLS_ctx.loading && !__VLS_ctx.error && !__VLS_ctx.documents.length),
    emptyMessage: "Aucun document trouvé pour ces critères.",
}, ...__VLS_functionalComponentArgsRest(__VLS_16));
const { default: __VLS_20 } = __VLS_18.slots;
if (__VLS_ctx.error && __VLS_ctx.documents.length) {
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
for (const [document] of __VLS_vFor((__VLS_ctx.documents))) {
    __VLS_asFunctionalElement1(__VLS_intrinsics.article, __VLS_intrinsics.article)({
        key: (document.id),
        ...{ class: "rounded-2xl border border-border bg-white p-5 shadow-sm" },
    });
    /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
    /** @type {__VLS_StyleScopedClasses['border']} */ ;
    /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
    /** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
    /** @type {__VLS_StyleScopedClasses['p-5']} */ ;
    /** @type {__VLS_StyleScopedClasses['shadow-sm']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between" },
    });
    /** @type {__VLS_StyleScopedClasses['flex']} */ ;
    /** @type {__VLS_StyleScopedClasses['flex-col']} */ ;
    /** @type {__VLS_StyleScopedClasses['gap-4']} */ ;
    /** @type {__VLS_StyleScopedClasses['lg:flex-row']} */ ;
    /** @type {__VLS_StyleScopedClasses['lg:items-start']} */ ;
    /** @type {__VLS_StyleScopedClasses['lg:justify-between']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "min-w-0 flex-1" },
    });
    /** @type {__VLS_StyleScopedClasses['min-w-0']} */ ;
    /** @type {__VLS_StyleScopedClasses['flex-1']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "flex flex-wrap items-center gap-2" },
    });
    /** @type {__VLS_StyleScopedClasses['flex']} */ ;
    /** @type {__VLS_StyleScopedClasses['flex-wrap']} */ ;
    /** @type {__VLS_StyleScopedClasses['items-center']} */ ;
    /** @type {__VLS_StyleScopedClasses['gap-2']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
        ...{ class: "rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700" },
    });
    /** @type {__VLS_StyleScopedClasses['rounded-full']} */ ;
    /** @type {__VLS_StyleScopedClasses['bg-slate-100']} */ ;
    /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
    /** @type {__VLS_StyleScopedClasses['py-1']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-xs']} */ ;
    /** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-slate-700']} */ ;
    (__VLS_ctx.documentTypeLabel(document.document_type));
    __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
        ...{ class: "rounded-full px-3 py-1 text-xs font-medium" },
        ...{ class: (__VLS_ctx.documentStatusClass(document.status)) },
    });
    /** @type {__VLS_StyleScopedClasses['rounded-full']} */ ;
    /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
    /** @type {__VLS_StyleScopedClasses['py-1']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-xs']} */ ;
    /** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
    (__VLS_ctx.documentStatusLabel(document.status));
    __VLS_asFunctionalElement1(__VLS_intrinsics.h3, __VLS_intrinsics.h3)({
        ...{ class: "mt-2 text-lg font-semibold" },
    });
    /** @type {__VLS_StyleScopedClasses['mt-2']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-lg']} */ ;
    /** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
    (document.title);
    if (document.comment) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
            ...{ class: "mt-2 text-sm text-slate-600" },
        });
        /** @type {__VLS_StyleScopedClasses['mt-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-slate-600']} */ ;
        (document.comment);
    }
    __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
        ...{ class: "mt-2 text-xs text-slate-500" },
    });
    /** @type {__VLS_StyleScopedClasses['mt-2']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-xs']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-slate-500']} */ ;
    (__VLS_ctx.formatDate(document.created_at));
    if (document.reviewed_at) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({});
        (__VLS_ctx.formatDate(document.reviewed_at));
    }
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "flex shrink-0 flex-wrap gap-2" },
    });
    /** @type {__VLS_StyleScopedClasses['flex']} */ ;
    /** @type {__VLS_StyleScopedClasses['shrink-0']} */ ;
    /** @type {__VLS_StyleScopedClasses['flex-wrap']} */ ;
    /** @type {__VLS_StyleScopedClasses['gap-2']} */ ;
    if (document.file) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.a, __VLS_intrinsics.a)({
            ...{ class: "inline-flex items-center rounded-xl border border-border px-4 py-2 text-sm font-medium" },
            href: (document.file),
            target: "_blank",
            rel: "noreferrer",
        });
        /** @type {__VLS_StyleScopedClasses['inline-flex']} */ ;
        /** @type {__VLS_StyleScopedClasses['items-center']} */ ;
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
        let __VLS_21;
        /** @ts-ignore @type { | typeof __VLS_components.Download} */
        Download;
        // @ts-ignore
        const __VLS_22 = __VLS_asFunctionalComponent1(__VLS_21, new __VLS_21({
            ...{ class: "mr-2 h-4 w-4" },
        }));
        const __VLS_23 = __VLS_22({
            ...{ class: "mr-2 h-4 w-4" },
        }, ...__VLS_functionalComponentArgsRest(__VLS_22));
        /** @type {__VLS_StyleScopedClasses['mr-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
    }
    if (__VLS_ctx.canReviewDocument(document)) {
        if (__VLS_ctx.reviewingId !== document.id) {
            __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
                ...{ onClick: (...[$event]) => {
                        if (!(__VLS_ctx.canReviewDocument(document)))
                            return;
                        if (!(__VLS_ctx.reviewingId !== document.id))
                            return;
                        __VLS_ctx.reviewingId = document.id;
                        // @ts-ignore
                        [uploadForm, uploadForm, uploadForm, onFileChange, saving, saving, applyFilters, applyFilters, applyFilters, applyFilters, search, statusFilter, typeFilter, loading, loading, error, error, error, error, error, documents, documents, documents, documents, documentTypeLabel, documentStatusClass, documentStatusLabel, formatDate, formatDate, canReviewDocument, reviewingId, reviewingId,];
                    } },
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
            __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
                ...{ onClick: (...[$event]) => {
                        if (!(__VLS_ctx.canReviewDocument(document)))
                            return;
                        if (!!(__VLS_ctx.reviewingId !== document.id))
                            return;
                        __VLS_ctx.reviewDocument(document, 'approve');
                        // @ts-ignore
                        [reviewDocument,];
                    } },
                ...{ class: "inline-flex items-center rounded-xl border border-emerald-200 px-4 py-2 text-sm text-emerald-700 disabled:opacity-60" },
                disabled: (__VLS_ctx.saving),
            });
            /** @type {__VLS_StyleScopedClasses['inline-flex']} */ ;
            /** @type {__VLS_StyleScopedClasses['items-center']} */ ;
            /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['border']} */ ;
            /** @type {__VLS_StyleScopedClasses['border-emerald-200']} */ ;
            /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-emerald-700']} */ ;
            /** @type {__VLS_StyleScopedClasses['disabled:opacity-60']} */ ;
            let __VLS_26;
            /** @ts-ignore @type { | typeof __VLS_components.Check} */
            Check;
            // @ts-ignore
            const __VLS_27 = __VLS_asFunctionalComponent1(__VLS_26, new __VLS_26({
                ...{ class: "mr-2 h-4 w-4" },
            }));
            const __VLS_28 = __VLS_27({
                ...{ class: "mr-2 h-4 w-4" },
            }, ...__VLS_functionalComponentArgsRest(__VLS_27));
            /** @type {__VLS_StyleScopedClasses['mr-2']} */ ;
            /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
            __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
                ...{ onClick: (...[$event]) => {
                        if (!(__VLS_ctx.canReviewDocument(document)))
                            return;
                        if (!!(__VLS_ctx.reviewingId !== document.id))
                            return;
                        __VLS_ctx.reviewDocument(document, 'reject');
                        // @ts-ignore
                        [saving, reviewDocument,];
                    } },
                ...{ class: "inline-flex items-center rounded-xl border border-red-200 px-4 py-2 text-sm text-red-700 disabled:opacity-60" },
                disabled: (__VLS_ctx.saving),
            });
            /** @type {__VLS_StyleScopedClasses['inline-flex']} */ ;
            /** @type {__VLS_StyleScopedClasses['items-center']} */ ;
            /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['border']} */ ;
            /** @type {__VLS_StyleScopedClasses['border-red-200']} */ ;
            /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-red-700']} */ ;
            /** @type {__VLS_StyleScopedClasses['disabled:opacity-60']} */ ;
            let __VLS_31;
            /** @ts-ignore @type { | typeof __VLS_components.X} */
            X;
            // @ts-ignore
            const __VLS_32 = __VLS_asFunctionalComponent1(__VLS_31, new __VLS_31({
                ...{ class: "mr-2 h-4 w-4" },
            }));
            const __VLS_33 = __VLS_32({
                ...{ class: "mr-2 h-4 w-4" },
            }, ...__VLS_functionalComponentArgsRest(__VLS_32));
            /** @type {__VLS_StyleScopedClasses['mr-2']} */ ;
            /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
            __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
                ...{ onClick: (...[$event]) => {
                        if (!(__VLS_ctx.canReviewDocument(document)))
                            return;
                        if (!!(__VLS_ctx.reviewingId !== document.id))
                            return;
                        __VLS_ctx.reviewingId = null;
                        // @ts-ignore
                        [saving, reviewingId,];
                    } },
                ...{ class: "rounded-xl border border-border px-4 py-2 text-sm" },
            });
            /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['border']} */ ;
            /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
            /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        }
    }
    if (__VLS_ctx.reviewingId === document.id) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "mt-4 border-t border-border pt-4" },
        });
        /** @type {__VLS_StyleScopedClasses['mt-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-t']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['pt-4']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.label, __VLS_intrinsics.label)({
            ...{ class: "text-sm font-medium text-slate-700" },
        });
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-slate-700']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.textarea)({
            value: (__VLS_ctx.reviewComment),
            ...{ class: "mt-2 min-h-20 w-full rounded-xl border border-border px-3 py-2.5 text-sm" },
            placeholder: "Motif ou remarques pour l’étudiant",
        });
        /** @type {__VLS_StyleScopedClasses['mt-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['min-h-20']} */ ;
        /** @type {__VLS_StyleScopedClasses['w-full']} */ ;
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    }
    // @ts-ignore
    [reviewingId, reviewComment,];
}
// @ts-ignore
[];
var __VLS_18;
const __VLS_36 = ListPagination;
// @ts-ignore
const __VLS_37 = __VLS_asFunctionalComponent1(__VLS_36, new __VLS_36({
    ...{ 'onPrevious': {} },
    ...{ 'onNext': {} },
    page: (__VLS_ctx.page),
    totalPages: (__VLS_ctx.totalPages),
    total: (__VLS_ctx.total),
    pageSize: (__VLS_ctx.PAGE_SIZE),
}));
const __VLS_38 = __VLS_37({
    ...{ 'onPrevious': {} },
    ...{ 'onNext': {} },
    page: (__VLS_ctx.page),
    totalPages: (__VLS_ctx.totalPages),
    total: (__VLS_ctx.total),
    pageSize: (__VLS_ctx.PAGE_SIZE),
}, ...__VLS_functionalComponentArgsRest(__VLS_37));
let __VLS_41;
const __VLS_42 = {
    /** @type {typeof __VLS_41.previous} */
    onPrevious: (__VLS_ctx.previousPage),
};
const __VLS_43 = {
    /** @type {typeof __VLS_41.next} */
    onNext: (__VLS_ctx.nextPage),
};
var __VLS_39;
var __VLS_40;
// @ts-ignore
[page, totalPages, total, PAGE_SIZE, previousPage, nextPage,];
const __VLS_export = (await import('vue')).defineComponent({});
export default {};
//# sourceMappingURL=DocumentsPage.vue.js.map