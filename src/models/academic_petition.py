"""Academic petition model."""

from dataclasses import dataclass

from .petition import Petition


@dataclass
class AcademicPetition(Petition):
    """Petition type for academic requests."""

    receiver: str = "Dean"
