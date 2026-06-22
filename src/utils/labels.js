const DOCUMENT_TYPE_LABELS = {
    CV: 'CV',
    CONVENTION: 'Convention de stage',
    REPORT: 'Rapport',
};
const DOCUMENT_STATUS_LABELS = {
    UPLOADED: 'Déposé',
    IN_REVIEW: 'En revue',
    APPROVED: 'Approuvé',
    REJECTED: 'Rejeté',
};
const INTERNSHIP_STATUS_LABELS = {
    ASSIGNED: 'Assigné',
    ACTIVE: 'En cours',
    COMPLETED: 'Terminé',
    CANCELLED: 'Annulé',
};
export function documentTypeLabel(type) {
    return type ? DOCUMENT_TYPE_LABELS[type] : 'Non renseigné';
}
export function documentStatusLabel(status) {
    if (typeof status === 'string' && status in DOCUMENT_STATUS_LABELS) {
        return DOCUMENT_STATUS_LABELS[status];
    }
    return typeof status === 'string' ? status : 'Inconnu';
}
export function internshipStatusLabel(status) {
    return status ? INTERNSHIP_STATUS_LABELS[status] : 'Statut inconnu';
}
export function internshipLabel(internship, offerTitles = {}) {
    const title = offerTitles[internship.offer];
    const dates = [internship.start_date, internship.end_date].filter(Boolean).join(' – ');
    const status = internshipStatusLabel(internship.status);
    if (title) {
        return dates ? `${title} · ${dates}` : title;
    }
    if (dates)
        return `Stage · ${dates} · ${status}`;
    return `Stage · ${status}`;
}
export function documentStatusClass(status) {
    switch (status) {
        case 'APPROVED':
            return 'bg-emerald-50 text-emerald-700';
        case 'REJECTED':
            return 'bg-red-50 text-red-700';
        case 'IN_REVIEW':
            return 'bg-amber-50 text-amber-700';
        default:
            return 'bg-slate-100 text-slate-700';
    }
}
//# sourceMappingURL=labels.js.map