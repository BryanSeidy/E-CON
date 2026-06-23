<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  ArrowRight,
  GraduationCap,
  Building2,
  Users,
  BookOpen,
  Shield,
  Clock,
  BarChart3,
  FileText,
  Bell,
  ChevronDown,
  CheckCircle2,
  Lock,
  Server,
  Eye,
  Zap,
  Target,
  TrendingUp,
  CalendarCheck,
  ClipboardList,
  MessageSquare,
  Star,
  Menu,
  X,
} from 'lucide-vue-next'

const router = useRouter()
const mobileMenuOpen = ref(false)

const openFaqIndex = ref<number | null>(null)
function toggleFaq(index: number) {
  openFaqIndex.value = openFaqIndex.value === index ? null : index
}

function navigateToLogin() {
  router.push('/login')
}

function scrollTo(id: string) {
  mobileMenuOpen.value = false
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

const navLinks = [
  { label: 'Fonctionnalites', target: 'fonctionnalites' },
  { label: 'Cibles', target: 'cibles' },
  { label: 'Securite', target: 'securite' },
  { label: 'FAQ', target: 'faq' },
]

const problems = [
  {
    icon: FileText,
    title: 'Suivi manuel et fragmente',
    description:
      'Les conventions, fiches de stage et rapports circulent par email ou en papier. Aucune tracabilite, aucune vision consolidee.',
  },
  {
    icon: Clock,
    title: 'Perte de temps administrative',
    description:
      'Les equipes pedagogiques passent des heures a collecter, verifier et relancer les documents de stage.',
  },
  {
    icon: Eye,
    title: 'Opacite du processus',
    description:
      'Etudiants, encadreurs et entreprises n\'ont aucune visibilite en temps reel sur l\'avancement des stages.',
  },
  {
    icon: Shield,
    title: 'Risques de conformite',
    description:
      'Sans outil centralise, les etablissements peinent a garantir la conformite reglementaire et la protection des donnees.',
  },
]

const targets = [
  {
    icon: GraduationCap,
    role: 'Universites et Instituts',
    benefits: [
      'Pilotage centralise de tous les stages',
      'Tableaux de bord en temps reel',
      'Conformite reglementaire automatisee',
      'Reduction de 70% du temps administratif',
    ],
  },
  {
    icon: Building2,
    role: 'Entreprises',
    benefits: [
      'Publication d\'offres qualifiees',
      'Gestion simplifiee des candidatures',
      'Suivi structure des stagiaires',
      'Evaluations normalisees',
    ],
  },
  {
    icon: Users,
    role: 'Etudiants',
    benefits: [
      'Acces a des offres verifiees',
      'Suivi clair de chaque etape',
      'Depot et signature de documents en ligne',
      'Journal de bord hebdomadaire integre',
    ],
  },
  {
    icon: BookOpen,
    role: 'Encadreurs',
    benefits: [
      'Vision complete sur les stagiaires encadres',
      'Validation des rapports en un clic',
      'Grilles d\'evaluation standardisees',
      'Notifications intelligentes',
    ],
  },
]

const features = [
  {
    icon: ClipboardList,
    title: 'Gestion des conventions',
    description:
      'Generation, signature electronique et archivage automatique des conventions de stage.',
  },
  {
    icon: BarChart3,
    title: 'Tableaux de bord intelligents',
    description:
      'Indicateurs par role, filtres avances et export de donnees pour un pilotage precis.',
  },
  {
    icon: FileText,
    title: 'Gestion documentaire',
    description:
      'Depot, validation et suivi de chaque document avec historique complet des versions.',
  },
  {
    icon: CalendarCheck,
    title: 'Journal de bord hebdomadaire',
    description:
      'Les etudiants consignent leurs activites. Les encadreurs valident et commentent en continu.',
  },
  {
    icon: Bell,
    title: 'Notifications contextuelles',
    description:
      'Alertes ciblees par role : echeances, validations requises, mises a jour de statut.',
  },
  {
    icon: Target,
    title: 'Evaluations structurees',
    description:
      'Grilles d\'evaluation personnalisables avec notation academique et professionnelle.',
  },
  {
    icon: Users,
    title: 'Gestion multi-roles',
    description:
      'RBAC granulaire : etudiant, encadreur academique, encadreur professionnel, administration, entreprise.',
  },
  {
    icon: TrendingUp,
    title: 'Reporting et analytics',
    description:
      'Rapports d\'activite, taux de placement, durees moyennes et indicateurs de performance.',
  },
]

const steps = [
  {
    number: '01',
    title: 'Configuration',
    description:
      'L\'universite configure ses programmes, periodes de stage et grilles d\'evaluation en quelques minutes.',
  },
  {
    number: '02',
    title: 'Publication',
    description:
      'Les entreprises publient leurs offres. Les etudiants postulent directement depuis la plateforme.',
  },
  {
    number: '03',
    title: 'Suivi',
    description:
      'Conventions generees automatiquement. Chaque acteur suit l\'avancement en temps reel depuis son tableau de bord.',
  },
  {
    number: '04',
    title: 'Evaluation',
    description:
      'A l\'issue du stage, les evaluations sont completees en ligne et les rapports archives durablement.',
  },
]

const reassuranceItems = [
  {
    icon: Lock,
    title: 'Chiffrement de bout en bout',
    description: 'Toutes les donnees sont chiffrees en transit (TLS 1.3) et au repos (AES-256).',
  },
  {
    icon: Shield,
    title: 'Conformite RGPD',
    description:
      'Hebergement en Europe, consentement explicite, droit a l\'oubli et portabilite des donnees.',
  },
  {
    icon: Server,
    title: 'Haute disponibilite',
    description:
      'Infrastructure redondante avec un SLA de 99.9%. Sauvegardes automatiques quotidiennes.',
  },
  {
    icon: Eye,
    title: 'Audit et tracabilite',
    description:
      'Chaque action est journalisee. Historique complet accessible aux administrateurs.',
  },
]

const testimonials = [
  {
    quote:
      'E-CON a transforme notre gestion des stages. Nous avons divise par trois le temps consacre au suivi administratif.',
    author: 'Dr. Amina K.',
    role: 'Directrice des stages',
    org: 'Institut Polytechnique',
  },
  {
    quote:
      'La visibilite en temps reel sur les candidatures et les evaluations nous permet de prendre de meilleures decisions.',
    author: 'Marc D.',
    role: 'Responsable RH',
    org: 'TechCorp Afrique',
  },
  {
    quote:
      'Tout est clair, du depot de candidature a la signature de convention. Je sais exactement ou j\'en suis.',
    author: 'Sarah L.',
    role: 'Etudiante en Master 2',
    org: 'Universite de Kinshasa',
  },
]

const faqs = [
  {
    question: 'E-CON est-il adapte a mon etablissement ?',
    answer:
      'E-CON est concu pour tous les etablissements d\'enseignement superieur : universites, ecoles d\'ingenieurs, instituts de formation professionnelle. La plateforme s\'adapte a vos processus existants.',
  },
  {
    question: 'Combien de temps faut-il pour deployer la plateforme ?',
    answer:
      'Le deploiement standard prend entre 2 et 4 semaines, incluant la configuration initiale, l\'import des donnees et la formation des equipes.',
  },
  {
    question: 'Mes donnees sont-elles securisees ?',
    answer:
      'Absolument. E-CON est heberge sur une infrastructure europeenne certifiee, avec chiffrement AES-256, conformite RGPD et sauvegardes quotidiennes.',
  },
  {
    question: 'Puis-je tester la plateforme avant de m\'engager ?',
    answer:
      'Oui. Nous proposons une demonstration personnalisee gratuite ainsi qu\'un environnement de test pour valider l\'adequation avec vos besoins.',
  },
  {
    question: 'Quel accompagnement proposez-vous ?',
    answer:
      'Chaque client beneficie d\'un chef de projet dedie, d\'une formation complete et d\'un support technique reactif par email et visioconference.',
  },
  {
    question: 'E-CON s\'integre-t-il avec nos outils existants ?',
    answer:
      'E-CON expose une API REST documentee (OpenAPI) qui permet l\'integration avec vos systemes d\'information, LMS ou ERP existants.',
  },
]

const stats = [
  { value: '12+', label: 'Etablissements partenaires' },
  { value: '8 000+', label: 'Stages geres' },
  { value: '95%', label: 'Taux de satisfaction' },
  { value: '-70%', label: 'Temps administratif' },
]
</script>

<template>
  <div class="min-h-screen bg-white text-ink antialiased">
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- NAVIGATION                                                        -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <nav
      class="fixed inset-x-0 top-0 z-50 border-b border-border/60 bg-white/80 backdrop-blur-lg"
    >
      <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <button
          class="text-xl font-bold tracking-tight text-slate-900"
          @click="scrollTo('hero')"
        >
          E-CON
        </button>

        <!-- Desktop links -->
        <div class="hidden items-center gap-8 md:flex">
          <button
            v-for="link in navLinks"
            :key="link.target"
            class="text-sm font-medium text-slate-600 transition-colors hover:text-slate-900"
            @click="scrollTo(link.target)"
          >
            {{ link.label }}
          </button>
          <button
            class="rounded-xl bg-slate-950 px-5 py-2.5 text-sm font-semibold text-white transition-shadow hover:shadow-lg hover:shadow-slate-950/20"
            @click="navigateToLogin"
          >
            Connexion
          </button>
        </div>

        <!-- Mobile hamburger -->
        <button class="md:hidden" @click="mobileMenuOpen = !mobileMenuOpen">
          <X v-if="mobileMenuOpen" class="h-5 w-5" />
          <Menu v-else class="h-5 w-5" />
        </button>
      </div>

      <!-- Mobile menu -->
      <div
        v-if="mobileMenuOpen"
        class="border-t border-border bg-white px-6 pb-6 pt-4 md:hidden"
      >
        <button
          v-for="link in navLinks"
          :key="link.target"
          class="block w-full py-3 text-left text-sm font-medium text-slate-600"
          @click="scrollTo(link.target)"
        >
          {{ link.label }}
        </button>
        <button
          class="mt-4 w-full rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white"
          @click="navigateToLogin"
        >
          Connexion
        </button>
      </div>
    </nav>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- HERO SECTION                                                       -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <section
      id="hero"
      class="relative overflow-hidden bg-gradient-to-b from-slate-50 to-white pb-20 pt-32 sm:pb-28 sm:pt-40"
    >
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-50/60 via-transparent to-transparent" />
      <div class="relative mx-auto max-w-5xl px-6 text-center">
        <p
          class="inline-block rounded-full border border-indigo-200 bg-indigo-50 px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.15em] text-indigo-700"
        >
          Plateforme SaaS pour la gestion des stages academiques
        </p>
        <h1
          class="mx-auto mt-8 max-w-4xl text-4xl font-extrabold leading-[1.1] tracking-tight text-slate-900 sm:text-5xl lg:text-6xl"
        >
          Digitalisez la gestion de vos stages.
          <span class="text-indigo-600">Simplement.</span>
        </h1>
        <p class="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-slate-600 sm:text-xl">
          E-CON centralise le pilotage, le suivi et l'evaluation des stages academiques
          pour les universites, les entreprises, les etudiants et les encadreurs
          -- sur une seule plateforme securisee.
        </p>
        <div class="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a
            href="#contact"
            class="group inline-flex items-center rounded-xl bg-indigo-600 px-7 py-3.5 text-sm font-semibold text-white shadow-lg shadow-indigo-600/25 transition-all hover:bg-indigo-700 hover:shadow-xl hover:shadow-indigo-600/30"
          >
            Demander une demo
            <ArrowRight class="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
          </a>
          <button
            class="inline-flex items-center rounded-xl border border-border px-7 py-3.5 text-sm font-semibold text-slate-700 transition-colors hover:bg-slate-50"
            @click="scrollTo('fonctionnalites')"
          >
            Decouvrir les fonctionnalites
          </button>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- SOCIAL PROOF STRIP                                                 -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <section class="border-y border-border/60 bg-slate-50 py-12">
      <div class="mx-auto max-w-6xl px-6">
        <p class="mb-8 text-center text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
          Chiffres cles
        </p>
        <div class="grid grid-cols-2 gap-8 sm:grid-cols-4">
          <div v-for="stat in stats" :key="stat.label" class="text-center">
            <p class="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">
              {{ stat.value }}
            </p>
            <p class="mt-1 text-sm text-slate-500">{{ stat.label }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- PROBLEMS SOLVED                                                    -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <section class="py-20 sm:py-28">
      <div class="mx-auto max-w-6xl px-6">
        <div class="mx-auto max-w-2xl text-center">
          <p
            class="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-600"
          >
            Le constat
          </p>
          <h2 class="mt-4 text-3xl font-bold tracking-tight sm:text-4xl">
            La gestion des stages ne peut plus reposer sur des outils generiques
          </h2>
          <p class="mt-4 text-base leading-relaxed text-slate-600">
            Tableurs, emails et documents papier generent des erreurs, des retards
            et une absence totale de tracabilite.
          </p>
        </div>
        <div class="mt-16 grid gap-8 sm:grid-cols-2">
          <div
            v-for="problem in problems"
            :key="problem.title"
            class="rounded-2xl border border-border bg-white p-8 shadow-sm transition-shadow hover:shadow-md"
          >
            <div
              class="flex h-11 w-11 items-center justify-center rounded-xl bg-red-50 text-red-600"
            >
              <component :is="problem.icon" class="h-5 w-5" />
            </div>
            <h3 class="mt-5 text-lg font-semibold">{{ problem.title }}</h3>
            <p class="mt-2 text-sm leading-relaxed text-slate-600">
              {{ problem.description }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- BENEFITS BY TARGET                                                 -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <section id="cibles" class="bg-slate-50 py-20 sm:py-28">
      <div class="mx-auto max-w-6xl px-6">
        <div class="mx-auto max-w-2xl text-center">
          <p
            class="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-600"
          >
            Pour chaque acteur
          </p>
          <h2 class="mt-4 text-3xl font-bold tracking-tight sm:text-4xl">
            Une plateforme, quatre experiences sur mesure
          </h2>
          <p class="mt-4 text-base leading-relaxed text-slate-600">
            Chaque profil dispose d'une interface dediee, adaptee a ses responsabilites
            et a ses objectifs.
          </p>
        </div>
        <div class="mt-16 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          <div
            v-for="target in targets"
            :key="target.role"
            class="rounded-2xl border border-border bg-white p-8 shadow-sm transition-shadow hover:shadow-md"
          >
            <div
              class="flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600"
            >
              <component :is="target.icon" class="h-5 w-5" />
            </div>
            <h3 class="mt-5 text-lg font-semibold">{{ target.role }}</h3>
            <ul class="mt-4 space-y-3">
              <li
                v-for="benefit in target.benefits"
                :key="benefit"
                class="flex items-start gap-2.5 text-sm text-slate-600"
              >
                <CheckCircle2 class="mt-0.5 h-4 w-4 flex-shrink-0 text-emerald-500" />
                <span>{{ benefit }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- KEY FEATURES                                                       -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <section id="fonctionnalites" class="py-20 sm:py-28">
      <div class="mx-auto max-w-6xl px-6">
        <div class="mx-auto max-w-2xl text-center">
          <p
            class="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-600"
          >
            Fonctionnalites
          </p>
          <h2 class="mt-4 text-3xl font-bold tracking-tight sm:text-4xl">
            Tout ce qu'il faut pour gerer les stages de A a Z
          </h2>
          <p class="mt-4 text-base leading-relaxed text-slate-600">
            Une suite complete d'outils concus pour couvrir l'integralite du cycle de stage,
            de la publication de l'offre a l'archivage du rapport final.
          </p>
        </div>
        <div class="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <div
            v-for="feature in features"
            :key="feature.title"
            class="rounded-2xl border border-border bg-white p-6 shadow-sm transition-shadow hover:shadow-md"
          >
            <div
              class="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600"
            >
              <component :is="feature.icon" class="h-5 w-5" />
            </div>
            <h3 class="mt-4 text-sm font-semibold">{{ feature.title }}</h3>
            <p class="mt-2 text-sm leading-relaxed text-slate-500">
              {{ feature.description }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- HOW IT WORKS                                                       -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <section class="bg-slate-950 py-20 text-white sm:py-28">
      <div class="mx-auto max-w-6xl px-6">
        <div class="mx-auto max-w-2xl text-center">
          <p
            class="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-400"
          >
            Processus
          </p>
          <h2 class="mt-4 text-3xl font-bold tracking-tight sm:text-4xl">
            Operationnel en quatre etapes
          </h2>
          <p class="mt-4 text-base leading-relaxed text-slate-400">
            De la configuration initiale a la cloture des stages, E-CON structure
            chaque phase pour vous.
          </p>
        </div>
        <div class="mt-16 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          <div v-for="step in steps" :key="step.number" class="relative">
            <p class="text-5xl font-extrabold text-indigo-500/30">{{ step.number }}</p>
            <h3 class="mt-4 text-lg font-semibold">{{ step.title }}</h3>
            <p class="mt-2 text-sm leading-relaxed text-slate-400">
              {{ step.description }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- SECURITY & COMPLIANCE                                              -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <section id="securite" class="py-20 sm:py-28">
      <div class="mx-auto max-w-6xl px-6">
        <div class="mx-auto max-w-2xl text-center">
          <p
            class="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-600"
          >
            Securite et conformite
          </p>
          <h2 class="mt-4 text-3xl font-bold tracking-tight sm:text-4xl">
            Vos donnees sont entre de bonnes mains
          </h2>
          <p class="mt-4 text-base leading-relaxed text-slate-600">
            La securite et la conformite sont au coeur de l'architecture d'E-CON.
            Chaque composant est concu pour proteger les donnees sensibles de vos
            etudiants et de vos institutions.
          </p>
        </div>
        <div class="mt-16 grid gap-8 sm:grid-cols-2">
          <div
            v-for="item in reassuranceItems"
            :key="item.title"
            class="flex gap-5 rounded-2xl border border-border bg-white p-8 shadow-sm"
          >
            <div
              class="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600"
            >
              <component :is="item.icon" class="h-5 w-5" />
            </div>
            <div>
              <h3 class="text-base font-semibold">{{ item.title }}</h3>
              <p class="mt-1 text-sm leading-relaxed text-slate-600">
                {{ item.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- PRODUCT DEMO / SCREENSHOT                                          -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <section class="bg-slate-50 py-20 sm:py-28">
      <div class="mx-auto max-w-6xl px-6">
        <div class="mx-auto max-w-2xl text-center">
          <p
            class="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-600"
          >
            Apercu produit
          </p>
          <h2 class="mt-4 text-3xl font-bold tracking-tight sm:text-4xl">
            Une interface pensee pour la productivite
          </h2>
          <p class="mt-4 text-base leading-relaxed text-slate-600">
            Chaque role accede a un tableau de bord personnalise. Indicateurs,
            actions prioritaires et notifications : tout est reuni en un seul
            endroit.
          </p>
        </div>
        <div
          class="mx-auto mt-12 max-w-4xl overflow-hidden rounded-2xl border border-border bg-white shadow-xl"
        >
          <div class="flex items-center gap-2 border-b border-border bg-slate-50 px-5 py-3">
            <span class="h-3 w-3 rounded-full bg-red-400" />
            <span class="h-3 w-3 rounded-full bg-amber-400" />
            <span class="h-3 w-3 rounded-full bg-emerald-400" />
            <span class="ml-4 text-xs text-slate-400">app.e-con.io/dashboard</span>
          </div>
          <div class="p-8 sm:p-12">
            <div class="grid gap-4 sm:grid-cols-3">
              <div class="rounded-xl border border-border bg-slate-50 p-6">
                <p class="text-xs font-semibold uppercase tracking-widest text-slate-400">
                  Stages actifs
                </p>
                <p class="mt-2 text-3xl font-bold text-indigo-600">247</p>
              </div>
              <div class="rounded-xl border border-border bg-slate-50 p-6">
                <p class="text-xs font-semibold uppercase tracking-widest text-slate-400">
                  Candidatures
                </p>
                <p class="mt-2 text-3xl font-bold text-slate-900">1 024</p>
              </div>
              <div class="rounded-xl border border-border bg-slate-50 p-6">
                <p class="text-xs font-semibold uppercase tracking-widest text-slate-400">
                  Taux de placement
                </p>
                <p class="mt-2 text-3xl font-bold text-emerald-600">89%</p>
              </div>
            </div>
            <div class="mt-6 space-y-3">
              <div class="h-4 w-full rounded-full bg-slate-100">
                <div class="h-4 w-3/4 rounded-full bg-indigo-500" />
              </div>
              <div class="h-4 w-full rounded-full bg-slate-100">
                <div class="h-4 w-1/2 rounded-full bg-emerald-500" />
              </div>
              <div class="h-4 w-full rounded-full bg-slate-100">
                <div class="h-4 w-5/6 rounded-full bg-amber-400" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- TESTIMONIALS                                                       -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <section class="py-20 sm:py-28">
      <div class="mx-auto max-w-6xl px-6">
        <div class="mx-auto max-w-2xl text-center">
          <p
            class="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-600"
          >
            Temoignages
          </p>
          <h2 class="mt-4 text-3xl font-bold tracking-tight sm:text-4xl">
            Ils nous font confiance
          </h2>
        </div>
        <div class="mt-16 grid gap-8 sm:grid-cols-3">
          <div
            v-for="testimonial in testimonials"
            :key="testimonial.author"
            class="flex flex-col rounded-2xl border border-border bg-white p-8 shadow-sm"
          >
            <div class="mb-4 flex gap-1">
              <Star
                v-for="i in 5"
                :key="i"
                class="h-4 w-4 fill-amber-400 text-amber-400"
              />
            </div>
            <blockquote class="flex-1 text-sm leading-relaxed text-slate-600">
              "{{ testimonial.quote }}"
            </blockquote>
            <div class="mt-6 border-t border-border pt-4">
              <p class="text-sm font-semibold text-slate-900">{{ testimonial.author }}</p>
              <p class="text-xs text-slate-500">
                {{ testimonial.role }}, {{ testimonial.org }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- FAQ                                                                -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <section id="faq" class="bg-slate-50 py-20 sm:py-28">
      <div class="mx-auto max-w-3xl px-6">
        <div class="text-center">
          <p
            class="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-600"
          >
            Questions frequentes
          </p>
          <h2 class="mt-4 text-3xl font-bold tracking-tight sm:text-4xl">
            Vous avez des questions ?
          </h2>
        </div>
        <div class="mt-12 space-y-3">
          <div
            v-for="(faq, index) in faqs"
            :key="index"
            class="overflow-hidden rounded-2xl border border-border bg-white shadow-sm"
          >
            <button
              class="flex w-full items-center justify-between px-6 py-5 text-left"
              @click="toggleFaq(index)"
            >
              <span class="pr-4 text-sm font-semibold">{{ faq.question }}</span>
              <ChevronDown
                class="h-4 w-4 flex-shrink-0 text-slate-400 transition-transform duration-200"
                :class="{ 'rotate-180': openFaqIndex === index }"
              />
            </button>
            <div
              v-if="openFaqIndex === index"
              class="border-t border-border px-6 pb-5 pt-4"
            >
              <p class="text-sm leading-relaxed text-slate-600">{{ faq.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- FINAL CTA                                                          -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <section
      id="contact"
      class="bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 py-20 text-white sm:py-28"
    >
      <div class="mx-auto max-w-3xl px-6 text-center">
        <h2 class="text-3xl font-bold tracking-tight sm:text-4xl">
          Pret a moderniser la gestion de vos stages ?
        </h2>
        <p class="mx-auto mt-5 max-w-xl text-base leading-relaxed text-slate-300">
          Demandez une demonstration personnalisee et decouvrez comment E-CON
          peut transformer votre processus en quelques semaines.
        </p>
        <div class="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a
            href="mailto:contact@e-con.io?subject=Demande%20de%20d%C3%A9mo%20E-CON"
            class="group inline-flex items-center rounded-xl bg-indigo-600 px-8 py-4 text-sm font-semibold text-white shadow-lg shadow-indigo-600/25 transition-all hover:bg-indigo-500 hover:shadow-xl hover:shadow-indigo-500/30"
          >
            Demander une demo gratuite
            <ArrowRight class="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
          </a>
          <a
            href="mailto:contact@e-con.io?subject=Contact%20E-CON"
            class="inline-flex items-center rounded-xl border border-white/20 px-8 py-4 text-sm font-semibold text-white transition-colors hover:bg-white/10"
          >
            Contacter l'equipe
          </a>
        </div>
        <p class="mt-8 text-xs text-slate-500">
          Sans engagement. Reponse sous 24 heures.
        </p>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- FOOTER                                                             -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <footer class="border-t border-border bg-white py-12">
      <div class="mx-auto max-w-6xl px-6">
        <div class="flex flex-col items-center justify-between gap-6 sm:flex-row">
          <div>
            <p class="text-lg font-bold tracking-tight text-slate-900">E-CON</p>
            <p class="mt-1 text-sm text-slate-500">
              Plateforme de gestion intelligente des stages academiques.
            </p>
          </div>
          <div class="flex items-center gap-6 text-sm text-slate-500">
            <button @click="scrollTo('fonctionnalites')" class="hover:text-slate-900 transition-colors">
              Fonctionnalites
            </button>
            <button @click="scrollTo('securite')" class="hover:text-slate-900 transition-colors">
              Securite
            </button>
            <button @click="scrollTo('faq')" class="hover:text-slate-900 transition-colors">
              FAQ
            </button>
            <button @click="scrollTo('contact')" class="hover:text-slate-900 transition-colors">
              Contact
            </button>
          </div>
        </div>
        <div class="mt-8 border-t border-border pt-8 text-center text-xs text-slate-400">
          &copy; {{ new Date().getFullYear() }} E-CON. Tous droits reserves.
        </div>
      </div>
    </footer>
  </div>
</template>
