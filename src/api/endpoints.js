import { api } from './http';
import { resourceClient } from './resource';
export const applicationsApi = resourceClient('/api/v1/applications/');
export const companiesApi = resourceClient('/api/v1/companies/');
export const companyMembershipsApi = resourceClient('/api/v1/company-memberships/');
export const departmentsApi = resourceClient('/api/v1/departments/');
export const documentsApi = resourceClient('/api/v1/documents/');
export const evaluationsApi = resourceClient('/api/v1/evaluations/');
export const institutionsApi = resourceClient('/api/v1/institutions/');
export const internshipsApi = resourceClient('/api/v1/internships/');
export const notificationsApi = resourceClient('/api/v1/notifications/');
export const offersApi = resourceClient('/api/v1/offers/');
export const weeklyLogsApi = resourceClient('/api/v1/weekly-logs/');
export const dashboardApi = { student: () => api.get('/dashboard/student/').then(r => r.data), company: () => api.get('/dashboard/company/').then(r => r.data), university: () => api.get('/dashboard/university/').then(r => r.data) };
//# sourceMappingURL=endpoints.js.map