"""Corporate-action domain contract required by IA-1C persistence ports."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CorporateAction:
    action_id: str
    listing_id: str
    effective_at: datetime
    action_type: str
