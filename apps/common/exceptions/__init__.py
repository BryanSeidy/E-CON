"""Centralized DRF exception handling."""

from __future__ import annotations

import logging
from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger(__name__)


def exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    """Convert Django ValidationErrors into DRF ValidationErrors.

    This prevents unhandled Django ValidationErrors from producing 500
    responses. All other exceptions are delegated to DRF's default handler.
    """
    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, "message_dict"):
            data = exc.message_dict
        else:
            data = exc.messages
        exc = DRFValidationError(detail=data)

    return drf_exception_handler(exc, context)
