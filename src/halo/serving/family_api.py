"""Family Companion web FastAPI backend (Phase 2).

Endpoints:
    GET  /health                  Liveness.
    GET  /info                    Version, model_id, commit.
    POST /api/v1/notify           Receive Medium or Hard alert from a HALO device.
    POST /api/v1/confirm          Family member confirmation of alert.
    GET  /api/v1/history          Paginated event history for authenticated family user.

Security model:
    - OAuth + OIDC authentication.
    - E2E encryption of alert payloads via libsodium sealed boxes.
    - Rate limiting on /notify per device.
    - Audit log of every API call.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class EventType(str, Enum):
    MEDIUM_RISK = "medium_risk"
    HARD_RISK = "hard_risk"


class NotifyPayload(BaseModel):
    user_id: str
    event_type: EventType
    category: str
    risk_score: int
    timestamp: datetime


def create_app() -> object:
    """Assemble the FastAPI application with all routes and middleware.

    Returns:
        FastAPI instance.
    """
    raise NotImplementedError


def main() -> None:
    """Run uvicorn for local dev."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
