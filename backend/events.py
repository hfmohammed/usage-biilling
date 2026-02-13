"""
Stub event publishing. Replace publish_event() with Kafka (or other broker) later.
"""

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

_published_events: list[dict[str, Any]] = []


def publish_event(event_type: str, payload: dict[str, Any]) -> None:
    """
    Publish an event. For now just logs and appends to _published_events.
    Later: send to Kafka / Azure Event Hubs.
    """
    event = {
        "event_type": event_type,
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    logger.info("Event published: %s", event_type, extra={"event": event})
    _published_events.append(event)


def get_published_events() -> list[dict[str, Any]]:
    """Return events published in this process (for tests or debugging)."""
    return list(_published_events)


def clear_published_events() -> None:
    """Clear the in-memory event list (e.g. between tests)."""
    _published_events.clear()
