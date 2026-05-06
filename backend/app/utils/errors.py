"""Error handling utilities and standardized error responses."""

from fastapi import HTTPException, status
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class APIError(HTTPException):
    """Base API error with standardized response format."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        code: str = "INTERNAL_ERROR",
        extra: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.detail = {
            "error": True,
            "message": detail,
            "code": code,
        }
        if extra:
            self.detail.update(extra)


class ValidationError(APIError):
    """Request validation error."""

    def __init__(self, detail: str, extra: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            code="VALIDATION_ERROR",
            extra=extra,
        )


class NotFoundError(APIError):
    """Resource not found error."""

    def __init__(self, resource: str, resource_id: Any = None):
        detail = f"{resource} not found"
        if resource_id:
            detail = f"{resource} with ID {resource_id} not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            code="NOT_FOUND",
        )


class UnauthorizedError(APIError):
    """Authentication error."""

    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            code="UNAUTHORIZED",
        )


class ForbiddenError(APIError):
    """Authorization error."""

    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            code="FORBIDDEN",
        )


class ConflictError(APIError):
    """Resource already exists error."""

    def __init__(self, resource: str, detail: Optional[str] = None):
        msg = detail or f"{resource} already exists"
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=msg,
            code="CONFLICT",
        )


class InternalServerError(APIError):
    """Internal server error."""

    def __init__(self, detail: str = "Internal server error", code: str = "INTERNAL_ERROR"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            code=code,
        )


def safe_operation(operation_name: str):
    """Decorator for safe error handling in async operations."""

    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except APIError:
                raise
            except ValueError as e:
                logger.error(f"{operation_name} validation error: {str(e)}")
                raise ValidationError(str(e))
            except KeyError as e:
                logger.error(f"{operation_name} missing key: {str(e)}")
                raise NotFoundError("Resource", str(e))
            except Exception as e:
                logger.error(f"{operation_name} error: {str(e)}", exc_info=True)
                raise InternalServerError(f"Failed to {operation_name}: {str(e)}")

        return wrapper

    return decorator


def log_error(operation: str, error: Exception) -> None:
    """Log error with context."""
    logger.error(f"Operation '{operation}' failed: {str(error)}", exc_info=True)
