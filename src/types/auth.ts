export type UserRole = 'STUDENT' | 'COMPANY_MEMBER' | 'ACADEMIC_SUPERVISOR' | 'HEAD_OF_PROGRAM' | 'UNIVERSITY_ADMIN' | 'SUPER_ADMIN'
export interface SessionUser { id?: string; email?: string; firstName?: string; lastName?: string; role?: UserRole }
