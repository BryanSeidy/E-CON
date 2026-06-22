import { applicationsApi, companiesApi, dashboardApi, documentsApi, evaluationsApi, internshipsApi, notificationsApi, offersApi, weeklyLogsApi } from '@/api/endpoints'
import { createResourceStore } from './resources'
export const useOffersStore = createResourceStore('offers', offersApi.list)
export const useApplicationsStore = createResourceStore('applications', applicationsApi.list)
export const useInternshipsStore = createResourceStore('internships', internshipsApi.list)
export const useDocumentsStore = createResourceStore('documents', documentsApi.list)
export const useEvaluationsStore = createResourceStore('evaluations', evaluationsApi.list)
export const useNotificationsStore = createResourceStore('notifications', notificationsApi.list)
export const useCompaniesStore = createResourceStore('companies', companiesApi.list)
export const useWeeklyLogsStore = createResourceStore('weeklyLogs', weeklyLogsApi.list)
export const useStudentDashboardStore = createResourceStore('studentDashboard', dashboardApi.student)
export const useCompanyDashboardStore = createResourceStore('companyDashboard', dashboardApi.company)
export const useUniversityDashboardStore = createResourceStore('universityDashboard', dashboardApi.university)
