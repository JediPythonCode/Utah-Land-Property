"""
Expired / withdrawn listing signals.

WFRMLS and most MLS systems expose expired or withdrawn status when credentials are present.
This module provides the structure; the autonomous scheduler can call pull_expired_listings()
once the WFRMLS token is configured.

Falls back to empty list.
"""
import logging
from typing import Any

logger = logging.getLogger("utah-desk.expired")

def pull_expired_listings(days: int = 30) -> list[dict[str, Any]]:
    """
    Placeholder for expired / withdrawn pulls.
    When WFRMLS credentials are set, filter StandardStatus in ('Expired', 'Withdrawn').
    """
    logger.info("Expired listing pull: waiting on WFRMLS credentials")
    return []
