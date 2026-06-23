import { createRouter, createWebHistory, type RouteLocationNormalized } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { UserRole } from '@/types/auth'
type Meta = { requiresAuth?: boolean; roles?: UserRole[] }
const Login = () => import('@/modules/auth/LoginPage.vue')
const Shell = () => import('@/layouts/AppShell.vue')
const Dashboard = () => import('@/pages/DashboardPage.vue')
const Placeholder = () => import('@/pages/PlaceholderPage.vue')
const route = (path: string, name: string, label: string, roles?: UserRole[]) => ({ path, name, component: Placeholder, meta: { requiresAuth: true, label, roles } })
export const router = createRouter({
  history: createWebHistory(), routes: [
    { path: '/login', name: 'login', component: Login, meta: { guest: true } },
    {
      path: '/', component: Shell, meta: { requiresAuth: true }, children: [
        { path: '', redirect: '/dashboard' },
        { path: 'dashboard', name: 'dashboard', component: Dashboard, meta: { requiresAuth: true, label: 'Dashboard' } },
        route('profile', 'profile', 'Mon profil'), route('offers', 'offers', 'Offres'), route('offers/:id', 'offer-detail', 'Détail offre'), route('applications', 'applications', 'Mes candidatures'), route('internships', 'internships', 'Mon stage'), route('documents', 'documents', 'Documents'), route('tracking/weekly-logs', 'weekly-logs', 'Journal hebdomadaire'), route('evaluations', 'evaluations', 'Evaluations'), route('notifications', 'notifications', 'Notifications'),
        route('company/profile', 'company-profile', 'Profil entreprise', ['COMPANY_MEMBER']), route('company/offers', 'company-offers', 'Offres entreprise', ['COMPANY_MEMBER']), route('company/applications', 'company-applications', 'Candidatures reçues', ['COMPANY_MEMBER']),
        route('university/students', 'university-students', 'Etudiants', ['UNIVERSITY_ADMIN', 'ACADEMIC_SUPERVISOR', 'HEAD_OF_PROGRAM']), route('university/internships', 'university-internships', 'Stages', ['UNIVERSITY_ADMIN', 'ACADEMIC_SUPERVISOR', 'HEAD_OF_PROGRAM'])
      ]
    },
    { path: '/:pathMatch(.*)*', redirect: '/dashboard' }
  ]
})
function canAccess(to: RouteLocationNormalized) { const auth = useAuthStore(); const meta = to.meta as Meta; if (!meta.roles?.length) return true; return Boolean(auth.role && meta.roles.includes(auth.role)) }
router.beforeEach((to) => { const auth = useAuthStore(); if (to.meta.requiresAuth && !auth.isAuthenticated) return { name: 'login', query: { redirect: to.fullPath } }; if (to.name === 'login' && auth.isAuthenticated) return { name: 'dashboard' }; if (!canAccess(to)) return { name: 'dashboard' } })
