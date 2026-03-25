"""Administrative petition model."""

from dataclasses import dataclass

from .petition import Petition


@dataclass
class AdministrativePetition(Petition):
    """Petition type for administrative requests."""

    receiver: str = "Administrative Office"
