"""Common abstract models and enums."""

from apps.common.models.base import (
    AuditModel,
    BaseModel,
    BaseSoftDeleteModel,
    SoftDeleteModel,
    TenantAwareModel,
    TimestampedModel,
    UUIDModel,
)
from apps.common.models.enums import (
    AIProcessingStatus,
    ApplicationStatus,
    AuditSource,
    ConventionStatus,
    DocumentStatus,
    EvaluationType,
    InternshipStatus,
    ProgramLevel,
    UserRole,
)

__all__ = [
    "AIProcessingStatus",
    "ApplicationStatus",
    "AuditModel",
    "AuditSource",
    "BaseModel",
    "BaseSoftDeleteModel",
    "ConventionStatus",
    "DocumentStatus",
    "EvaluationType",
    "InternshipStatus",
    "ProgramLevel",
    "SoftDeleteModel",
    "TenantAwareModel",
    "TimestampedModel",
    "UUIDModel",
    "UserRole",
]
