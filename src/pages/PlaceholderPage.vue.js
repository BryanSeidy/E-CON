import { computed, onMounted, reactive, ref, watch } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { AlertCircle, Check, ChevronLeft, ChevronRight, Edit3, Loader2, Plus, Search, Trash2, X } from 'lucide-vue-next';
import { applicationsApi, companiesApi, internshipsApi, offersApi } from '@/api/endpoints';
import { useAuthStore } from '@/stores/auth';
const route = useRoute();
const auth = useAuthStore();
const loading = ref(false);
const saving = ref(false);
const error = ref('');
const search = ref('');
const page = ref(1);
const total = ref(0);
const offers = ref([]);
const applications = ref([]);
const internships = ref([]);
const companies = ref([]);
const selectedOffer = ref(null);
const editingOfferId = ref(null);
const coverLetter = ref('');
const offerForm = reactive({ company: '', title: '', description: '', location: '', required_skills: '', start_date: '', end_date: '', is_active: true });
const activeView = computed(() => String(route.name ?? ''));
const isList = computed(() => ['offers', 'company-offers'].includes(activeView.value));
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / 20)));
function resetState() { error.value = ''; selectedOffer.value = null; applications.value = []; internships.value = []; offers.value = []; total.value = 0; }
function setError(message = 'Une erreur est survenue pendant le chargement.') { error.value = message; }
function resetOfferForm(company = '') { Object.assign(offerForm, { company, title: '', description: '', location: '', required_skills: '', start_date: '', end_date: '', is_active: true }); editingOfferId.value = null; }
function editOffer(offer) { Object.assign(offerForm, { company: offer.company, title: offer.title, description: offer.description, location: offer.location ?? '', required_skills: offer.required_skills ?? '', start_date: offer.start_date ?? '', end_date: offer.end_date ?? '', is_active: offer.is_active ?? true }); editingOfferId.value = offer.id; }
async function loadCompanies() { companies.value = (await companiesApi.list()).results; if (!offerForm.company && companies.value[0])
    offerForm.company = companies.value[0].id; }
async function loadOffers() { const response = await offersApi.list({ page: page.value, search: search.value || undefined }); offers.value = response.results; total.value = response.count; }
async function loadApplications() { const response = await applicationsApi.list({ page: page.value, search: search.value || undefined }); applications.value = response.results; total.value = response.count; }
async function loadInternships() { const response = await internshipsApi.list({ page: page.value, search: search.value || undefined }); internships.value = response.results; total.value = response.count; }
async function loadOfferDetail() { selectedOffer.value = await offersApi.retrieve(String(route.params.id)); }
async function loadCurrentView() {
    loading.value = true;
    resetState();
    try {
        if (activeView.value === 'offers' || activeView.value === 'company-offers') {
            if (activeView.value === 'company-offers')
                await loadCompanies();
            await loadOffers();
        }
        if (activeView.value === 'offer-detail')
            await loadOfferDetail();
        if (['applications', 'company-applications'].includes(activeView.value))
            await loadApplications();
        if (['internships', 'university-internships'].includes(activeView.value))
            await loadInternships();
    }
    catch {
        setError();
    }
    finally {
        loading.value = false;
    }
}
async function submitApplication() { if (!selectedOffer.value)
    return; saving.value = true; try {
    await applicationsApi.create({ offer: selectedOffer.value.id, cover_letter: coverLetter.value });
    coverLetter.value = '';
}
catch {
    setError('La candidature n’a pas pu être envoyée.');
}
finally {
    saving.value = false;
} }
async function saveOffer() { saving.value = true; try {
    const payload = { ...offerForm, start_date: offerForm.start_date || null, end_date: offerForm.end_date || null };
    editingOfferId.value ? await offersApi.update(editingOfferId.value, payload) : await offersApi.create(payload);
    resetOfferForm(offerForm.company);
    await loadOffers();
}
catch {
    setError('L’offre n’a pas pu être enregistrée.');
}
finally {
    saving.value = false;
} }
async function deleteOffer(id) { saving.value = true; try {
    await offersApi.remove(id);
    await loadOffers();
}
catch {
    setError('L’offre n’a pas pu être supprimée.');
}
finally {
    saving.value = false;
} }
async function reviewApplication(application, action) { saving.value = true; try {
    await applicationsApi.action(application.id, action);
    await loadApplications();
}
catch {
    setError('La candidature n’a pas pu être mise à jour.');
}
finally {
    saving.value = false;
} }
function nextPage() { if (page.value < totalPages.value)
    page.value += 1; }
function previousPage() { if (page.value > 1)
    page.value -= 1; }
watch(() => route.fullPath, () => { page.value = 1; resetOfferForm(); void loadCurrentView(); });
watch([page], () => { if (isList.value || ['applications', 'company-applications', 'internships', 'university-internships'].includes(activeView.value))
    void loadCurrentView(); });
onMounted(loadCurrentView);
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
__VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
    ...{ class: "text-sm font-semibold uppercase tracking-wide text-slate-500" },
});
/** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
/** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
/** @type {__VLS_StyleScopedClasses['uppercase']} */ ;
/** @type {__VLS_StyleScopedClasses['tracking-wide']} */ ;
/** @type {__VLS_StyleScopedClasses['text-slate-500']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.h2, __VLS_intrinsics.h2)({
    ...{ class: "mt-2 text-3xl font-bold tracking-tight" },
});
/** @type {__VLS_StyleScopedClasses['mt-2']} */ ;
/** @type {__VLS_StyleScopedClasses['text-3xl']} */ ;
/** @type {__VLS_StyleScopedClasses['font-bold']} */ ;
/** @type {__VLS_StyleScopedClasses['tracking-tight']} */ ;
(__VLS_ctx.route.meta.label);
__VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
    ...{ class: "mt-3 max-w-3xl text-slate-600" },
});
/** @type {__VLS_StyleScopedClasses['mt-3']} */ ;
/** @type {__VLS_StyleScopedClasses['max-w-3xl']} */ ;
/** @type {__VLS_StyleScopedClasses['text-slate-600']} */ ;
if (__VLS_ctx.activeView === 'profile' || __VLS_ctx.activeView === 'university-students') {
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "rounded-2xl border border-amber-200 bg-amber-50 p-6 text-amber-900" },
    });
    /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
    /** @type {__VLS_StyleScopedClasses['border']} */ ;
    /** @type {__VLS_StyleScopedClasses['border-amber-200']} */ ;
    /** @type {__VLS_StyleScopedClasses['bg-amber-50']} */ ;
    /** @type {__VLS_StyleScopedClasses['p-6']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-amber-900']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "flex gap-3" },
    });
    /** @type {__VLS_StyleScopedClasses['flex']} */ ;
    /** @type {__VLS_StyleScopedClasses['gap-3']} */ ;
    let __VLS_0;
    /** @ts-ignore @type { | typeof __VLS_components.AlertCircle} */
    AlertCircle;
    // @ts-ignore
    const __VLS_1 = __VLS_asFunctionalComponent1(__VLS_0, new __VLS_0({
        ...{ class: "mt-0.5 h-5 w-5 shrink-0" },
    }));
    const __VLS_2 = __VLS_1({
        ...{ class: "mt-0.5 h-5 w-5 shrink-0" },
    }, ...__VLS_functionalComponentArgsRest(__VLS_1));
    /** @type {__VLS_StyleScopedClasses['mt-0.5']} */ ;
    /** @type {__VLS_StyleScopedClasses['h-5']} */ ;
    /** @type {__VLS_StyleScopedClasses['w-5']} */ ;
    /** @type {__VLS_StyleScopedClasses['shrink-0']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({});
    __VLS_asFunctionalElement1(__VLS_intrinsics.h3, __VLS_intrinsics.h3)({
        ...{ class: "font-semibold" },
    });
    /** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
        ...{ class: "mt-1 text-sm" },
    });
    /** @type {__VLS_StyleScopedClasses['mt-1']} */ ;
    /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
    if (__VLS_ctx.activeView === 'profile') {
        __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
            ...{ class: "mt-4 text-sm" },
        });
        /** @type {__VLS_StyleScopedClasses['mt-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
            ...{ class: "font-medium" },
        });
        /** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
        (__VLS_ctx.auth.user?.email || __VLS_ctx.auth.user?.id || 'Utilisateur authentifié');
    }
}
else {
    if (['offers', 'company-offers', 'applications', 'company-applications', 'internships', 'university-internships'].includes(__VLS_ctx.activeView)) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "flex flex-col gap-3 rounded-2xl border border-border bg-white p-4 md:flex-row md:items-center md:justify-between" },
        });
        /** @type {__VLS_StyleScopedClasses['flex']} */ ;
        /** @type {__VLS_StyleScopedClasses['flex-col']} */ ;
        /** @type {__VLS_StyleScopedClasses['gap-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
        /** @type {__VLS_StyleScopedClasses['p-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['md:flex-row']} */ ;
        /** @type {__VLS_StyleScopedClasses['md:items-center']} */ ;
        /** @type {__VLS_StyleScopedClasses['md:justify-between']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.label, __VLS_intrinsics.label)({
            ...{ class: "relative block w-full md:max-w-md" },
        });
        /** @type {__VLS_StyleScopedClasses['relative']} */ ;
        /** @type {__VLS_StyleScopedClasses['block']} */ ;
        /** @type {__VLS_StyleScopedClasses['w-full']} */ ;
        /** @type {__VLS_StyleScopedClasses['md:max-w-md']} */ ;
        let __VLS_5;
        /** @ts-ignore @type { | typeof __VLS_components.Search} */
        Search;
        // @ts-ignore
        const __VLS_6 = __VLS_asFunctionalComponent1(__VLS_5, new __VLS_5({
            ...{ class: "absolute left-3 top-3 h-4 w-4 text-slate-400" },
        }));
        const __VLS_7 = __VLS_6({
            ...{ class: "absolute left-3 top-3 h-4 w-4 text-slate-400" },
        }, ...__VLS_functionalComponentArgsRest(__VLS_6));
        /** @type {__VLS_StyleScopedClasses['absolute']} */ ;
        /** @type {__VLS_StyleScopedClasses['left-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['top-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-slate-400']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.input)({
            ...{ onKeyup: (...[$event]) => {
                    if (!!(__VLS_ctx.activeView === 'profile' || __VLS_ctx.activeView === 'university-students'))
                        return;
                    if (!(['offers', 'company-offers', 'applications', 'company-applications', 'internships', 'university-internships'].includes(__VLS_ctx.activeView)))
                        return;
                    __VLS_ctx.page = 1;
                    __VLS_ctx.loadCurrentView();
                    // @ts-ignore
                    [route, activeView, activeView, activeView, activeView, auth, auth, page, loadCurrentView,];
                } },
            ...{ class: "w-full rounded-xl border border-border py-2.5 pl-10 pr-3 text-sm" },
            placeholder: "Rechercher",
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
        __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
            ...{ onClick: (...[$event]) => {
                    if (!!(__VLS_ctx.activeView === 'profile' || __VLS_ctx.activeView === 'university-students'))
                        return;
                    if (!(['offers', 'company-offers', 'applications', 'company-applications', 'internships', 'university-internships'].includes(__VLS_ctx.activeView)))
                        return;
                    __VLS_ctx.page = 1;
                    __VLS_ctx.loadCurrentView();
                    // @ts-ignore
                    [page, loadCurrentView, search,];
                } },
            ...{ class: "rounded-xl border border-border px-4 py-2 text-sm font-medium" },
        });
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
    }
    if (__VLS_ctx.activeView === 'company-offers') {
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
        (__VLS_ctx.editingOfferId ? 'Modifier une offre' : 'Créer une offre');
        __VLS_asFunctionalElement1(__VLS_intrinsics.form, __VLS_intrinsics.form)({
            ...{ onSubmit: (__VLS_ctx.saveOffer) },
            ...{ class: "mt-4 grid gap-4 md:grid-cols-2" },
        });
        /** @type {__VLS_StyleScopedClasses['mt-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['grid']} */ ;
        /** @type {__VLS_StyleScopedClasses['gap-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['md:grid-cols-2']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.select, __VLS_intrinsics.select)({
            value: (__VLS_ctx.offerForm.company),
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
        for (const [company] of __VLS_vFor((__VLS_ctx.companies))) {
            __VLS_asFunctionalElement1(__VLS_intrinsics.option, __VLS_intrinsics.option)({
                key: (company.id),
                value: (company.id),
            });
            (company.name);
            // @ts-ignore
            [activeView, editingOfferId, saveOffer, offerForm, companies,];
        }
        __VLS_asFunctionalElement1(__VLS_intrinsics.input)({
            required: true,
            ...{ class: "rounded-xl border border-border px-3 py-2.5 text-sm" },
            placeholder: "Titre",
        });
        (__VLS_ctx.offerForm.title);
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.input)({
            ...{ class: "rounded-xl border border-border px-3 py-2.5 text-sm" },
            placeholder: "Localisation",
        });
        (__VLS_ctx.offerForm.location);
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.input)({
            ...{ class: "rounded-xl border border-border px-3 py-2.5 text-sm" },
            placeholder: "Compétences requises",
        });
        (__VLS_ctx.offerForm.required_skills);
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.input)({
            type: "date",
            ...{ class: "rounded-xl border border-border px-3 py-2.5 text-sm" },
        });
        (__VLS_ctx.offerForm.start_date);
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.input)({
            type: "date",
            ...{ class: "rounded-xl border border-border px-3 py-2.5 text-sm" },
        });
        (__VLS_ctx.offerForm.end_date);
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.textarea)({
            value: (__VLS_ctx.offerForm.description),
            required: true,
            ...{ class: "min-h-28 rounded-xl border border-border px-3 py-2.5 text-sm md:col-span-2" },
            placeholder: "Description",
        });
        /** @type {__VLS_StyleScopedClasses['min-h-28']} */ ;
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['md:col-span-2']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "flex items-center gap-3 md:col-span-2" },
        });
        /** @type {__VLS_StyleScopedClasses['flex']} */ ;
        /** @type {__VLS_StyleScopedClasses['items-center']} */ ;
        /** @type {__VLS_StyleScopedClasses['gap-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['md:col-span-2']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
            ...{ class: "rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-60" },
            disabled: (__VLS_ctx.saving),
        });
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['bg-slate-950']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-white']} */ ;
        /** @type {__VLS_StyleScopedClasses['disabled:opacity-60']} */ ;
        if (!__VLS_ctx.editingOfferId) {
            let __VLS_10;
            /** @ts-ignore @type { | typeof __VLS_components.Plus} */
            Plus;
            // @ts-ignore
            const __VLS_11 = __VLS_asFunctionalComponent1(__VLS_10, new __VLS_10({
                ...{ class: "mr-2 inline h-4 w-4" },
            }));
            const __VLS_12 = __VLS_11({
                ...{ class: "mr-2 inline h-4 w-4" },
            }, ...__VLS_functionalComponentArgsRest(__VLS_11));
            /** @type {__VLS_StyleScopedClasses['mr-2']} */ ;
            /** @type {__VLS_StyleScopedClasses['inline']} */ ;
            /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
        }
        else {
            let __VLS_15;
            /** @ts-ignore @type { | typeof __VLS_components.Edit3} */
            Edit3;
            // @ts-ignore
            const __VLS_16 = __VLS_asFunctionalComponent1(__VLS_15, new __VLS_15({
                ...{ class: "mr-2 inline h-4 w-4" },
            }));
            const __VLS_17 = __VLS_16({
                ...{ class: "mr-2 inline h-4 w-4" },
            }, ...__VLS_functionalComponentArgsRest(__VLS_16));
            /** @type {__VLS_StyleScopedClasses['mr-2']} */ ;
            /** @type {__VLS_StyleScopedClasses['inline']} */ ;
            /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
        }
        if (__VLS_ctx.editingOfferId) {
            __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
                ...{ onClick: (...[$event]) => {
                        if (!!(__VLS_ctx.activeView === 'profile' || __VLS_ctx.activeView === 'university-students'))
                            return;
                        if (!(__VLS_ctx.activeView === 'company-offers'))
                            return;
                        if (!(__VLS_ctx.editingOfferId))
                            return;
                        __VLS_ctx.resetOfferForm(__VLS_ctx.offerForm.company);
                        // @ts-ignore
                        [editingOfferId, editingOfferId, offerForm, offerForm, offerForm, offerForm, offerForm, offerForm, offerForm, saving, resetOfferForm,];
                    } },
                type: "button",
                ...{ class: "rounded-xl border border-border px-4 py-2.5 text-sm" },
            });
            /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['border']} */ ;
            /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
            /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        }
    }
    if (__VLS_ctx.loading) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "grid gap-4 md:grid-cols-2" },
        });
        /** @type {__VLS_StyleScopedClasses['grid']} */ ;
        /** @type {__VLS_StyleScopedClasses['gap-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['md:grid-cols-2']} */ ;
        for (const [i] of __VLS_vFor((4))) {
            __VLS_asFunctionalElement1(__VLS_intrinsics.div)({
                key: (i),
                ...{ class: "h-40 animate-pulse rounded-2xl bg-slate-200" },
            });
            /** @type {__VLS_StyleScopedClasses['h-40']} */ ;
            /** @type {__VLS_StyleScopedClasses['animate-pulse']} */ ;
            /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['bg-slate-200']} */ ;
            // @ts-ignore
            [loading,];
        }
    }
    else if (__VLS_ctx.error) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "rounded-2xl border border-red-200 bg-red-50 p-6 text-red-700" },
        });
        /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-red-200']} */ ;
        /** @type {__VLS_StyleScopedClasses['bg-red-50']} */ ;
        /** @type {__VLS_StyleScopedClasses['p-6']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-red-700']} */ ;
        (__VLS_ctx.error);
    }
    else if (__VLS_ctx.activeView === 'offer-detail' && __VLS_ctx.selectedOffer) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "grid gap-6 lg:grid-cols-[1fr_24rem]" },
        });
        /** @type {__VLS_StyleScopedClasses['grid']} */ ;
        /** @type {__VLS_StyleScopedClasses['gap-6']} */ ;
        /** @type {__VLS_StyleScopedClasses['lg:grid-cols-[1fr_24rem]']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.article, __VLS_intrinsics.article)({
            ...{ class: "rounded-2xl border border-border bg-white p-8 shadow-sm" },
        });
        /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
        /** @type {__VLS_StyleScopedClasses['p-8']} */ ;
        /** @type {__VLS_StyleScopedClasses['shadow-sm']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
            ...{ class: "text-sm font-medium text-slate-500" },
        });
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-slate-500']} */ ;
        (__VLS_ctx.selectedOffer.location || 'Localisation non renseignée');
        __VLS_asFunctionalElement1(__VLS_intrinsics.h3, __VLS_intrinsics.h3)({
            ...{ class: "mt-2 text-3xl font-bold" },
        });
        /** @type {__VLS_StyleScopedClasses['mt-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-3xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['font-bold']} */ ;
        (__VLS_ctx.selectedOffer.title);
        __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
            ...{ class: "mt-6 whitespace-pre-line leading-7 text-slate-700" },
        });
        /** @type {__VLS_StyleScopedClasses['mt-6']} */ ;
        /** @type {__VLS_StyleScopedClasses['whitespace-pre-line']} */ ;
        /** @type {__VLS_StyleScopedClasses['leading-7']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-slate-700']} */ ;
        (__VLS_ctx.selectedOffer.description);
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "mt-6 rounded-xl bg-slate-50 p-4 text-sm text-slate-600" },
        });
        /** @type {__VLS_StyleScopedClasses['mt-6']} */ ;
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['bg-slate-50']} */ ;
        /** @type {__VLS_StyleScopedClasses['p-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-slate-600']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
            ...{ class: "font-medium" },
        });
        /** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
        (__VLS_ctx.selectedOffer.required_skills || 'Non renseignées');
        __VLS_asFunctionalElement1(__VLS_intrinsics.form, __VLS_intrinsics.form)({
            ...{ onSubmit: (__VLS_ctx.submitApplication) },
            ...{ class: "rounded-2xl border border-border bg-white p-6 shadow-sm" },
        });
        /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
        /** @type {__VLS_StyleScopedClasses['p-6']} */ ;
        /** @type {__VLS_StyleScopedClasses['shadow-sm']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.h3, __VLS_intrinsics.h3)({
            ...{ class: "font-semibold" },
        });
        /** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.textarea)({
            value: (__VLS_ctx.coverLetter),
            ...{ class: "mt-4 min-h-40 w-full rounded-xl border border-border p-3 text-sm" },
            placeholder: "Lettre de motivation",
        });
        /** @type {__VLS_StyleScopedClasses['mt-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['min-h-40']} */ ;
        /** @type {__VLS_StyleScopedClasses['w-full']} */ ;
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['p-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
            ...{ class: "mt-4 w-full rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-60" },
            disabled: (__VLS_ctx.saving),
        });
        /** @type {__VLS_StyleScopedClasses['mt-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['w-full']} */ ;
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['bg-slate-950']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-white']} */ ;
        /** @type {__VLS_StyleScopedClasses['disabled:opacity-60']} */ ;
        if (__VLS_ctx.saving) {
            let __VLS_20;
            /** @ts-ignore @type { | typeof __VLS_components.Loader2} */
            Loader2;
            // @ts-ignore
            const __VLS_21 = __VLS_asFunctionalComponent1(__VLS_20, new __VLS_20({
                ...{ class: "mr-2 inline h-4 w-4 animate-spin" },
            }));
            const __VLS_22 = __VLS_21({
                ...{ class: "mr-2 inline h-4 w-4 animate-spin" },
            }, ...__VLS_functionalComponentArgsRest(__VLS_21));
            /** @type {__VLS_StyleScopedClasses['mr-2']} */ ;
            /** @type {__VLS_StyleScopedClasses['inline']} */ ;
            /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['animate-spin']} */ ;
        }
    }
    else if (['offers', 'company-offers'].includes(__VLS_ctx.activeView)) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "grid gap-4 md:grid-cols-2" },
        });
        /** @type {__VLS_StyleScopedClasses['grid']} */ ;
        /** @type {__VLS_StyleScopedClasses['gap-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['md:grid-cols-2']} */ ;
        for (const [offer] of __VLS_vFor((__VLS_ctx.offers))) {
            __VLS_asFunctionalElement1(__VLS_intrinsics.article, __VLS_intrinsics.article)({
                key: (offer.id),
                ...{ class: "rounded-2xl border border-border bg-white p-6 shadow-sm" },
            });
            /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['border']} */ ;
            /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
            /** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
            /** @type {__VLS_StyleScopedClasses['p-6']} */ ;
            /** @type {__VLS_StyleScopedClasses['shadow-sm']} */ ;
            __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
                ...{ class: "flex items-start justify-between gap-4" },
            });
            /** @type {__VLS_StyleScopedClasses['flex']} */ ;
            /** @type {__VLS_StyleScopedClasses['items-start']} */ ;
            /** @type {__VLS_StyleScopedClasses['justify-between']} */ ;
            /** @type {__VLS_StyleScopedClasses['gap-4']} */ ;
            __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({});
            __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
                ...{ class: "text-sm text-slate-500" },
            });
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-slate-500']} */ ;
            (offer.location || 'Localisation non renseignée');
            __VLS_asFunctionalElement1(__VLS_intrinsics.h3, __VLS_intrinsics.h3)({
                ...{ class: "mt-1 text-xl font-semibold" },
            });
            /** @type {__VLS_StyleScopedClasses['mt-1']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
            (offer.title);
            __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
                ...{ class: "rounded-full bg-slate-100 px-3 py-1 text-xs font-medium" },
            });
            /** @type {__VLS_StyleScopedClasses['rounded-full']} */ ;
            /** @type {__VLS_StyleScopedClasses['bg-slate-100']} */ ;
            /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
            /** @type {__VLS_StyleScopedClasses['py-1']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-xs']} */ ;
            /** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
            (offer.is_active ? 'Active' : 'Inactive');
            __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
                ...{ class: "mt-4 line-clamp-3 text-sm leading-6 text-slate-600" },
            });
            /** @type {__VLS_StyleScopedClasses['mt-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['line-clamp-3']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
            /** @type {__VLS_StyleScopedClasses['leading-6']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-slate-600']} */ ;
            (offer.description);
            __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
                ...{ class: "mt-5 flex flex-wrap gap-2" },
            });
            /** @type {__VLS_StyleScopedClasses['mt-5']} */ ;
            /** @type {__VLS_StyleScopedClasses['flex']} */ ;
            /** @type {__VLS_StyleScopedClasses['flex-wrap']} */ ;
            /** @type {__VLS_StyleScopedClasses['gap-2']} */ ;
            let __VLS_25;
            /** @ts-ignore @type { | typeof __VLS_components.RouterLink | typeof __VLS_components.RouterLink} */
            RouterLink;
            // @ts-ignore
            const __VLS_26 = __VLS_asFunctionalComponent1(__VLS_25, new __VLS_25({
                ...{ class: "rounded-xl bg-slate-950 px-4 py-2 text-sm font-semibold text-white" },
                to: (`/offers/${offer.id}`),
            }));
            const __VLS_27 = __VLS_26({
                ...{ class: "rounded-xl bg-slate-950 px-4 py-2 text-sm font-semibold text-white" },
                to: (`/offers/${offer.id}`),
            }, ...__VLS_functionalComponentArgsRest(__VLS_26));
            /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['bg-slate-950']} */ ;
            /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
            /** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-white']} */ ;
            const { default: __VLS_30 } = __VLS_28.slots;
            // @ts-ignore
            [activeView, activeView, saving, saving, error, error, selectedOffer, selectedOffer, selectedOffer, selectedOffer, selectedOffer, submitApplication, coverLetter, offers,];
            var __VLS_28;
            if (__VLS_ctx.activeView === 'company-offers') {
                __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
                    ...{ onClick: (...[$event]) => {
                            if (!!(__VLS_ctx.activeView === 'profile' || __VLS_ctx.activeView === 'university-students'))
                                return;
                            if (!!(__VLS_ctx.loading))
                                return;
                            if (!!(__VLS_ctx.error))
                                return;
                            if (!!(__VLS_ctx.activeView === 'offer-detail' && __VLS_ctx.selectedOffer))
                                return;
                            if (!(['offers', 'company-offers'].includes(__VLS_ctx.activeView)))
                                return;
                            if (!(__VLS_ctx.activeView === 'company-offers'))
                                return;
                            __VLS_ctx.editOffer(offer);
                            // @ts-ignore
                            [activeView, editOffer,];
                        } },
                    ...{ class: "rounded-xl border border-border px-4 py-2 text-sm" },
                });
                /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
                /** @type {__VLS_StyleScopedClasses['border']} */ ;
                /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
                /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
                /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
                /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
                let __VLS_31;
                /** @ts-ignore @type { | typeof __VLS_components.Edit3} */
                Edit3;
                // @ts-ignore
                const __VLS_32 = __VLS_asFunctionalComponent1(__VLS_31, new __VLS_31({
                    ...{ class: "mr-2 inline h-4 w-4" },
                }));
                const __VLS_33 = __VLS_32({
                    ...{ class: "mr-2 inline h-4 w-4" },
                }, ...__VLS_functionalComponentArgsRest(__VLS_32));
                /** @type {__VLS_StyleScopedClasses['mr-2']} */ ;
                /** @type {__VLS_StyleScopedClasses['inline']} */ ;
                /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
                /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
                __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
                    ...{ onClick: (...[$event]) => {
                            if (!!(__VLS_ctx.activeView === 'profile' || __VLS_ctx.activeView === 'university-students'))
                                return;
                            if (!!(__VLS_ctx.loading))
                                return;
                            if (!!(__VLS_ctx.error))
                                return;
                            if (!!(__VLS_ctx.activeView === 'offer-detail' && __VLS_ctx.selectedOffer))
                                return;
                            if (!(['offers', 'company-offers'].includes(__VLS_ctx.activeView)))
                                return;
                            if (!(__VLS_ctx.activeView === 'company-offers'))
                                return;
                            __VLS_ctx.deleteOffer(offer.id);
                            // @ts-ignore
                            [deleteOffer,];
                        } },
                    ...{ class: "rounded-xl border border-red-200 px-4 py-2 text-sm text-red-700" },
                });
                /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
                /** @type {__VLS_StyleScopedClasses['border']} */ ;
                /** @type {__VLS_StyleScopedClasses['border-red-200']} */ ;
                /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
                /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
                /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
                /** @type {__VLS_StyleScopedClasses['text-red-700']} */ ;
                let __VLS_36;
                /** @ts-ignore @type { | typeof __VLS_components.Trash2} */
                Trash2;
                // @ts-ignore
                const __VLS_37 = __VLS_asFunctionalComponent1(__VLS_36, new __VLS_36({
                    ...{ class: "mr-2 inline h-4 w-4" },
                }));
                const __VLS_38 = __VLS_37({
                    ...{ class: "mr-2 inline h-4 w-4" },
                }, ...__VLS_functionalComponentArgsRest(__VLS_37));
                /** @type {__VLS_StyleScopedClasses['mr-2']} */ ;
                /** @type {__VLS_StyleScopedClasses['inline']} */ ;
                /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
                /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
            }
            // @ts-ignore
            [];
        }
        if (!__VLS_ctx.offers.length) {
            __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
                ...{ class: "rounded-2xl border border-border bg-white p-10 text-center text-slate-500 md:col-span-2" },
            });
            /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['border']} */ ;
            /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
            /** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
            /** @type {__VLS_StyleScopedClasses['p-10']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-center']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-slate-500']} */ ;
            /** @type {__VLS_StyleScopedClasses['md:col-span-2']} */ ;
        }
    }
    else if (['applications', 'company-applications'].includes(__VLS_ctx.activeView)) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "space-y-3" },
        });
        /** @type {__VLS_StyleScopedClasses['space-y-3']} */ ;
        for (const [application] of __VLS_vFor((__VLS_ctx.applications))) {
            __VLS_asFunctionalElement1(__VLS_intrinsics.article, __VLS_intrinsics.article)({
                key: (application.id),
                ...{ class: "rounded-2xl border border-border bg-white p-5 shadow-sm" },
            });
            /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['border']} */ ;
            /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
            /** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
            /** @type {__VLS_StyleScopedClasses['p-5']} */ ;
            /** @type {__VLS_StyleScopedClasses['shadow-sm']} */ ;
            __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
                ...{ class: "flex flex-col gap-4 md:flex-row md:items-center md:justify-between" },
            });
            /** @type {__VLS_StyleScopedClasses['flex']} */ ;
            /** @type {__VLS_StyleScopedClasses['flex-col']} */ ;
            /** @type {__VLS_StyleScopedClasses['gap-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['md:flex-row']} */ ;
            /** @type {__VLS_StyleScopedClasses['md:items-center']} */ ;
            /** @type {__VLS_StyleScopedClasses['md:justify-between']} */ ;
            __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({});
            __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
                ...{ class: "text-sm text-slate-500" },
            });
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-slate-500']} */ ;
            __VLS_asFunctionalElement1(__VLS_intrinsics.h3, __VLS_intrinsics.h3)({
                ...{ class: "font-semibold" },
            });
            /** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
            (application.id);
            __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
                ...{ class: "mt-1 text-sm text-slate-600" },
            });
            /** @type {__VLS_StyleScopedClasses['mt-1']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-slate-600']} */ ;
            (application.status);
            __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
                ...{ class: "flex flex-wrap gap-2" },
            });
            /** @type {__VLS_StyleScopedClasses['flex']} */ ;
            /** @type {__VLS_StyleScopedClasses['flex-wrap']} */ ;
            /** @type {__VLS_StyleScopedClasses['gap-2']} */ ;
            let __VLS_41;
            /** @ts-ignore @type { | typeof __VLS_components.RouterLink | typeof __VLS_components.RouterLink} */
            RouterLink;
            // @ts-ignore
            const __VLS_42 = __VLS_asFunctionalComponent1(__VLS_41, new __VLS_41({
                ...{ class: "rounded-xl border border-border px-4 py-2 text-sm" },
                to: (`/offers/${application.offer}`),
            }));
            const __VLS_43 = __VLS_42({
                ...{ class: "rounded-xl border border-border px-4 py-2 text-sm" },
                to: (`/offers/${application.offer}`),
            }, ...__VLS_functionalComponentArgsRest(__VLS_42));
            /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['border']} */ ;
            /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
            /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
            /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
            const { default: __VLS_46 } = __VLS_44.slots;
            // @ts-ignore
            [activeView, offers, applications,];
            var __VLS_44;
            if (__VLS_ctx.activeView === 'company-applications') {
                __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
                    ...{ onClick: (...[$event]) => {
                            if (!!(__VLS_ctx.activeView === 'profile' || __VLS_ctx.activeView === 'university-students'))
                                return;
                            if (!!(__VLS_ctx.loading))
                                return;
                            if (!!(__VLS_ctx.error))
                                return;
                            if (!!(__VLS_ctx.activeView === 'offer-detail' && __VLS_ctx.selectedOffer))
                                return;
                            if (!!(['offers', 'company-offers'].includes(__VLS_ctx.activeView)))
                                return;
                            if (!(['applications', 'company-applications'].includes(__VLS_ctx.activeView)))
                                return;
                            if (!(__VLS_ctx.activeView === 'company-applications'))
                                return;
                            __VLS_ctx.reviewApplication(application, 'accept');
                            // @ts-ignore
                            [activeView, reviewApplication,];
                        } },
                    ...{ class: "rounded-xl border border-emerald-200 px-4 py-2 text-sm text-emerald-700" },
                });
                /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
                /** @type {__VLS_StyleScopedClasses['border']} */ ;
                /** @type {__VLS_StyleScopedClasses['border-emerald-200']} */ ;
                /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
                /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
                /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
                /** @type {__VLS_StyleScopedClasses['text-emerald-700']} */ ;
                let __VLS_47;
                /** @ts-ignore @type { | typeof __VLS_components.Check} */
                Check;
                // @ts-ignore
                const __VLS_48 = __VLS_asFunctionalComponent1(__VLS_47, new __VLS_47({
                    ...{ class: "mr-2 inline h-4 w-4" },
                }));
                const __VLS_49 = __VLS_48({
                    ...{ class: "mr-2 inline h-4 w-4" },
                }, ...__VLS_functionalComponentArgsRest(__VLS_48));
                /** @type {__VLS_StyleScopedClasses['mr-2']} */ ;
                /** @type {__VLS_StyleScopedClasses['inline']} */ ;
                /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
                /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
                __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
                    ...{ onClick: (...[$event]) => {
                            if (!!(__VLS_ctx.activeView === 'profile' || __VLS_ctx.activeView === 'university-students'))
                                return;
                            if (!!(__VLS_ctx.loading))
                                return;
                            if (!!(__VLS_ctx.error))
                                return;
                            if (!!(__VLS_ctx.activeView === 'offer-detail' && __VLS_ctx.selectedOffer))
                                return;
                            if (!!(['offers', 'company-offers'].includes(__VLS_ctx.activeView)))
                                return;
                            if (!(['applications', 'company-applications'].includes(__VLS_ctx.activeView)))
                                return;
                            if (!(__VLS_ctx.activeView === 'company-applications'))
                                return;
                            __VLS_ctx.reviewApplication(application, 'reject');
                            // @ts-ignore
                            [reviewApplication,];
                        } },
                    ...{ class: "rounded-xl border border-red-200 px-4 py-2 text-sm text-red-700" },
                });
                /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
                /** @type {__VLS_StyleScopedClasses['border']} */ ;
                /** @type {__VLS_StyleScopedClasses['border-red-200']} */ ;
                /** @type {__VLS_StyleScopedClasses['px-4']} */ ;
                /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
                /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
                /** @type {__VLS_StyleScopedClasses['text-red-700']} */ ;
                let __VLS_52;
                /** @ts-ignore @type { | typeof __VLS_components.X} */
                X;
                // @ts-ignore
                const __VLS_53 = __VLS_asFunctionalComponent1(__VLS_52, new __VLS_52({
                    ...{ class: "mr-2 inline h-4 w-4" },
                }));
                const __VLS_54 = __VLS_53({
                    ...{ class: "mr-2 inline h-4 w-4" },
                }, ...__VLS_functionalComponentArgsRest(__VLS_53));
                /** @type {__VLS_StyleScopedClasses['mr-2']} */ ;
                /** @type {__VLS_StyleScopedClasses['inline']} */ ;
                /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
                /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
            }
            // @ts-ignore
            [];
        }
        if (!__VLS_ctx.applications.length) {
            __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
                ...{ class: "rounded-2xl border border-border bg-white p-10 text-center text-slate-500" },
            });
            /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['border']} */ ;
            /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
            /** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
            /** @type {__VLS_StyleScopedClasses['p-10']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-center']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-slate-500']} */ ;
        }
    }
    else if (['internships', 'university-internships'].includes(__VLS_ctx.activeView)) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "space-y-3" },
        });
        /** @type {__VLS_StyleScopedClasses['space-y-3']} */ ;
        for (const [internship] of __VLS_vFor((__VLS_ctx.internships))) {
            __VLS_asFunctionalElement1(__VLS_intrinsics.article, __VLS_intrinsics.article)({
                key: (internship.id),
                ...{ class: "rounded-2xl border border-border bg-white p-5 shadow-sm" },
            });
            /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['border']} */ ;
            /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
            /** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
            /** @type {__VLS_StyleScopedClasses['p-5']} */ ;
            /** @type {__VLS_StyleScopedClasses['shadow-sm']} */ ;
            __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
                ...{ class: "flex flex-col gap-2 md:flex-row md:items-center md:justify-between" },
            });
            /** @type {__VLS_StyleScopedClasses['flex']} */ ;
            /** @type {__VLS_StyleScopedClasses['flex-col']} */ ;
            /** @type {__VLS_StyleScopedClasses['gap-2']} */ ;
            /** @type {__VLS_StyleScopedClasses['md:flex-row']} */ ;
            /** @type {__VLS_StyleScopedClasses['md:items-center']} */ ;
            /** @type {__VLS_StyleScopedClasses['md:justify-between']} */ ;
            __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({});
            __VLS_asFunctionalElement1(__VLS_intrinsics.h3, __VLS_intrinsics.h3)({
                ...{ class: "font-semibold" },
            });
            /** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
            (internship.id);
            __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
                ...{ class: "text-sm text-slate-600" },
            });
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-slate-600']} */ ;
            (internship.status);
            __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
                ...{ class: "text-sm text-slate-500" },
            });
            /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-slate-500']} */ ;
            (internship.start_date || 'Début non renseigné');
            (internship.end_date || 'Fin non renseignée');
            // @ts-ignore
            [activeView, applications, internships,];
        }
        if (!__VLS_ctx.internships.length) {
            __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
                ...{ class: "rounded-2xl border border-border bg-white p-10 text-center text-slate-500" },
            });
            /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
            /** @type {__VLS_StyleScopedClasses['border']} */ ;
            /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
            /** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
            /** @type {__VLS_StyleScopedClasses['p-10']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-center']} */ ;
            /** @type {__VLS_StyleScopedClasses['text-slate-500']} */ ;
        }
    }
    if (['offers', 'company-offers', 'applications', 'company-applications', 'internships', 'university-internships'].includes(__VLS_ctx.activeView) && __VLS_ctx.total > 20) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "flex items-center justify-between rounded-2xl border border-border bg-white p-4" },
        });
        /** @type {__VLS_StyleScopedClasses['flex']} */ ;
        /** @type {__VLS_StyleScopedClasses['items-center']} */ ;
        /** @type {__VLS_StyleScopedClasses['justify-between']} */ ;
        /** @type {__VLS_StyleScopedClasses['rounded-2xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
        /** @type {__VLS_StyleScopedClasses['p-4']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
            ...{ onClick: (__VLS_ctx.previousPage) },
            ...{ class: "rounded-xl border border-border px-3 py-2 text-sm disabled:opacity-50" },
            disabled: (__VLS_ctx.page === 1),
        });
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['disabled:opacity-50']} */ ;
        let __VLS_57;
        /** @ts-ignore @type { | typeof __VLS_components.ChevronLeft} */
        ChevronLeft;
        // @ts-ignore
        const __VLS_58 = __VLS_asFunctionalComponent1(__VLS_57, new __VLS_57({
            ...{ class: "mr-1 inline h-4 w-4" },
        }));
        const __VLS_59 = __VLS_58({
            ...{ class: "mr-1 inline h-4 w-4" },
        }, ...__VLS_functionalComponentArgsRest(__VLS_58));
        /** @type {__VLS_StyleScopedClasses['mr-1']} */ ;
        /** @type {__VLS_StyleScopedClasses['inline']} */ ;
        /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
            ...{ class: "text-sm text-slate-500" },
        });
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-slate-500']} */ ;
        (__VLS_ctx.page);
        (__VLS_ctx.totalPages);
        __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
            ...{ onClick: (__VLS_ctx.nextPage) },
            ...{ class: "rounded-xl border border-border px-3 py-2 text-sm disabled:opacity-50" },
            disabled: (__VLS_ctx.page === __VLS_ctx.totalPages),
        });
        /** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
        /** @type {__VLS_StyleScopedClasses['border']} */ ;
        /** @type {__VLS_StyleScopedClasses['border-border']} */ ;
        /** @type {__VLS_StyleScopedClasses['px-3']} */ ;
        /** @type {__VLS_StyleScopedClasses['py-2']} */ ;
        /** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
        /** @type {__VLS_StyleScopedClasses['disabled:opacity-50']} */ ;
        let __VLS_62;
        /** @ts-ignore @type { | typeof __VLS_components.ChevronRight} */
        ChevronRight;
        // @ts-ignore
        const __VLS_63 = __VLS_asFunctionalComponent1(__VLS_62, new __VLS_62({
            ...{ class: "ml-1 inline h-4 w-4" },
        }));
        const __VLS_64 = __VLS_63({
            ...{ class: "ml-1 inline h-4 w-4" },
        }, ...__VLS_functionalComponentArgsRest(__VLS_63));
        /** @type {__VLS_StyleScopedClasses['ml-1']} */ ;
        /** @type {__VLS_StyleScopedClasses['inline']} */ ;
        /** @type {__VLS_StyleScopedClasses['h-4']} */ ;
        /** @type {__VLS_StyleScopedClasses['w-4']} */ ;
    }
}
// @ts-ignore
[activeView, page, page, page, internships, total, previousPage, totalPages, totalPages, nextPage,];
const __VLS_export = (await import('vue')).defineComponent({});
export default {};
//# sourceMappingURL=PlaceholderPage.vue.js.map