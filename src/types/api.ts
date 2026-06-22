/* Auto-generated from backend OpenAPI schema. Do not edit by hand. */
export type UUID = string
export type ISODateTime = string

export interface Application {
  readonly id: string
  offer: string
  readonly student: string
  readonly status: unknown
  cover_letter?: string
  readonly reviewed_by: string | null
  readonly reviewed_at: string | null
  readonly created_at: string
  readonly updated_at: string
}

export interface ApplicationRequest {
  offer: string
  cover_letter?: string
}

export type ApplicationStatusEnum = 'PENDING' | 'REVIEWED' | 'ACCEPTED' | 'REJECTED'

export interface Company {
  readonly id: string
  name: string
  description?: string
  website?: string
  city?: string
  country?: string
  is_active?: boolean
  readonly created_at: string
  readonly updated_at: string
}

export interface CompanyMembership {
  readonly id: string
  company: string
  user: string
  title?: string
  is_owner?: boolean
  readonly created_at: string
  readonly updated_at: string
}

export interface CompanyMembershipRequest {
  company: string
  user: string
  title?: string
  is_owner?: boolean
}

export interface CompanyRequest {
  name: string
  description?: string
  website?: string
  city?: string
  country?: string
  is_active?: boolean
}

export interface DashboardSummary {
  applications?: number
  pending_applications?: number
  active_offers?: number
  assigned_internships?: number
  active_internships?: number
  completed_internships?: number
  documents?: number
  documents_to_review?: number
  rejected_documents?: number
  weekly_logs?: number
  unread_notifications?: number
}

export interface Department {
  readonly id: string
  institution: string
  name: string
  code: string
  readonly created_at: string
  readonly updated_at: string
}

export interface DepartmentRequest {
  institution: string
  name: string
  code: string
}

export interface Document {
  readonly id: string
  internship?: string | null
  readonly uploaded_by: string
  document_type?: DocumentTypeEnum
  title: string
  file: string
  readonly status: unknown
  comment?: string
  readonly reviewed_by: string | null
  readonly reviewed_at: string | null
  readonly created_at: string
  readonly updated_at: string
}

export interface DocumentRequest {
  internship?: string | null
  document_type?: DocumentTypeEnum
  title: string
  file: string
  comment?: string
}

export type DocumentStatusEnum = 'UPLOADED' | 'IN_REVIEW' | 'APPROVED' | 'REJECTED'

export type DocumentTypeEnum = 'CV' | 'CONVENTION' | 'REPORT'

export interface Evaluation {
  readonly id: string
  internship: string
  readonly evaluator: string
  evaluation_type: EvaluationTypeEnum
  score: number
  comment?: string
  readonly submitted_at: string | null
  readonly created_at: string
  readonly updated_at: string
}

export interface EvaluationRequest {
  internship: string
  evaluation_type: EvaluationTypeEnum
  score: number
  comment?: string
}

export type EvaluationTypeEnum = 'ACADEMIC' | 'PROFESSIONAL'

export interface Institution {
  readonly id: string
  name: string
  code: string
  country?: string
  city?: string
  is_active?: boolean
  readonly created_at: string
  readonly updated_at: string
}

export interface InstitutionRequest {
  name: string
  code: string
  country?: string
  city?: string
  is_active?: boolean
}

export interface Internship {
  readonly id: string
  readonly application: string
  readonly offer: string
  readonly student: string
  readonly company: string
  academic_supervisor?: string | null
  status?: InternshipStatusEnum
  start_date?: string | null
  end_date?: string | null
  readonly created_at: string
  readonly updated_at: string
}

export interface InternshipRequest {
  academic_supervisor?: string | null
  status?: InternshipStatusEnum
  start_date?: string | null
  end_date?: string | null
}

export type InternshipStatusEnum = 'ASSIGNED' | 'ACTIVE' | 'COMPLETED' | 'CANCELLED'

export interface Notification {
  readonly id: string
  readonly recipient: string
  title: string
  message: string
  is_read?: boolean
  readonly read_at: string | null
  readonly created_at: string
  readonly updated_at: string
}

export interface NotificationRequest {
  title: string
  message: string
  is_read?: boolean
}

export interface Offer {
  readonly id: string
  company: string
  title: string
  description: string
  location?: string
  required_skills?: string
  start_date?: string | null
  end_date?: string | null
  is_active?: boolean
  readonly created_at: string
  readonly updated_at: string
}

export interface OfferRequest {
  company: string
  title: string
  description: string
  location?: string
  required_skills?: string
  start_date?: string | null
  end_date?: string | null
  is_active?: boolean
}

export interface PaginatedApplicationList {
  count: number
  next?: string | null
  previous?: string | null
  results: Array<Application>
}

export interface PaginatedCompanyList {
  count: number
  next?: string | null
  previous?: string | null
  results: Array<Company>
}

export interface PaginatedCompanyMembershipList {
  count: number
  next?: string | null
  previous?: string | null
  results: Array<CompanyMembership>
}

export interface PaginatedDepartmentList {
  count: number
  next?: string | null
  previous?: string | null
  results: Array<Department>
}

export interface PaginatedDocumentList {
  count: number
  next?: string | null
  previous?: string | null
  results: Array<Document>
}

export interface PaginatedEvaluationList {
  count: number
  next?: string | null
  previous?: string | null
  results: Array<Evaluation>
}

export interface PaginatedInstitutionList {
  count: number
  next?: string | null
  previous?: string | null
  results: Array<Institution>
}

export interface PaginatedInternshipList {
  count: number
  next?: string | null
  previous?: string | null
  results: Array<Internship>
}

export interface PaginatedNotificationList {
  count: number
  next?: string | null
  previous?: string | null
  results: Array<Notification>
}

export interface PaginatedOfferList {
  count: number
  next?: string | null
  previous?: string | null
  results: Array<Offer>
}

export interface PaginatedWeeklyLogList {
  count: number
  next?: string | null
  previous?: string | null
  results: Array<WeeklyLog>
}

export interface PatchedApplicationRequest {
  offer?: string
  cover_letter?: string
}

export interface PatchedCompanyMembershipRequest {
  company?: string
  user?: string
  title?: string
  is_owner?: boolean
}

export interface PatchedCompanyRequest {
  name?: string
  description?: string
  website?: string
  city?: string
  country?: string
  is_active?: boolean
}

export interface PatchedDepartmentRequest {
  institution?: string
  name?: string
  code?: string
}

export interface PatchedDocumentRequest {
  internship?: string | null
  document_type?: DocumentTypeEnum
  title?: string
  file?: string
  comment?: string
}

export interface PatchedEvaluationRequest {
  internship?: string
  evaluation_type?: EvaluationTypeEnum
  score?: number
  comment?: string
}

export interface PatchedInstitutionRequest {
  name?: string
  code?: string
  country?: string
  city?: string
  is_active?: boolean
}

export interface PatchedInternshipRequest {
  academic_supervisor?: string | null
  status?: InternshipStatusEnum
  start_date?: string | null
  end_date?: string | null
}

export interface PatchedNotificationRequest {
  title?: string
  message?: string
  is_read?: boolean
}

export interface PatchedOfferRequest {
  company?: string
  title?: string
  description?: string
  location?: string
  required_skills?: string
  start_date?: string | null
  end_date?: string | null
  is_active?: boolean
}

export interface PatchedWeeklyLogRequest {
  internship?: string
  week_start?: string
  activities?: string
  blockers?: string
  next_steps?: string
}

export interface TokenObtainPair {
  readonly access: string
  readonly refresh: string
}

export interface TokenObtainPairRequest {
  email: string
  password: string
}

export interface TokenRefresh {
  readonly access: string
  refresh: string
}

export interface TokenRefreshRequest {
  refresh: string
}

export interface WeeklyLog {
  readonly id: string
  internship: string
  readonly student: string
  week_start: string
  activities: string
  blockers?: string
  next_steps?: string
  readonly submitted_at: string | null
  readonly created_at: string
  readonly updated_at: string
}

export interface WeeklyLogRequest {
  internship: string
  week_start: string
  activities: string
  blockers?: string
  next_steps?: string
}
