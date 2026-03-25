"""Administrative petition model."""

from dataclasses import dataclass

from .petition import Petition


@dataclass
class AdministrativePetition(Petition):
    """Petition type for administrative requests."""

    petition_type: str = "administrative"
    receiver: str = "Administrative Office"
    attachment_required: bool = False
