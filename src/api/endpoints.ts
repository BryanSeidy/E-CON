import { api } from './http'
import { resourceClient } from './resource'
import type { Application, ApplicationRequest, Company, CompanyMembership, CompanyMembershipRequest, CompanyRequest, DashboardSummary, Department, DepartmentRequest, Document, DocumentRequest, Evaluation, EvaluationRequest, Institution, InstitutionRequest, Internship, InternshipRequest, Notification, NotificationRequest, Offer, OfferRequest, PaginatedApplicationList, PaginatedCompanyList, PaginatedCompanyMembershipList, PaginatedDepartmentList, PaginatedDocumentList, PaginatedEvaluationList, PaginatedInstitutionList, PaginatedInternshipList, PaginatedNotificationList, PaginatedOfferList, PaginatedWeeklyLogList, WeeklyLog, WeeklyLogRequest } from '@/types/api'
export const applicationsApi = resourceClient<PaginatedApplicationList, Application, ApplicationRequest>('/api/v1/applications/')
export const companiesApi = resourceClient<PaginatedCompanyList, Company, CompanyRequest>('/api/v1/companies/')
export const companyMembershipsApi = resourceClient<PaginatedCompanyMembershipList, CompanyMembership, CompanyMembershipRequest>('/api/v1/company-memberships/')
export const departmentsApi = resourceClient<PaginatedDepartmentList, Department, DepartmentRequest>('/api/v1/departments/')
export const documentsApi = resourceClient<PaginatedDocumentList, Document, DocumentRequest | FormData>('/api/v1/documents/')
export const evaluationsApi = resourceClient<PaginatedEvaluationList, Evaluation, EvaluationRequest>('/api/v1/evaluations/')
export const institutionsApi = resourceClient<PaginatedInstitutionList, Institution, InstitutionRequest>('/api/v1/institutions/')
export const internshipsApi = resourceClient<PaginatedInternshipList, Internship, InternshipRequest>('/api/v1/internships/')
export const notificationsApi = resourceClient<PaginatedNotificationList, Notification, NotificationRequest>('/api/v1/notifications/')
export const offersApi = resourceClient<PaginatedOfferList, Offer, OfferRequest>('/api/v1/offers/')
export const weeklyLogsApi = resourceClient<PaginatedWeeklyLogList, WeeklyLog, WeeklyLogRequest>('/api/v1/weekly-logs/')
export const dashboardApi = { student: () => api.get<DashboardSummary>('/dashboard/student/').then(r=>r.data), company: () => api.get<DashboardSummary>('/dashboard/company/').then(r=>r.data), university: () => api.get<DashboardSummary>('/dashboard/university/').then(r=>r.data) }
