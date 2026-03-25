"""Base petition model and prototype support."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field


@dataclass
class Petition:
    """Base petition object."""

    title: str
    body: str
    petitioner: str
    created_by: str 
    status: str = "draft"
    attachment_required: bool = False
    attachments: list[str] = field(default_factory=list)

    def clone(self) -> "Petition":
        """Return a deep copy for template-based petition creation."""
        return deepcopy(self)
