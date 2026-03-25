"""Academic petition model."""

from dataclasses import dataclass

from .petition import Petition

@dataclass
class AcademicPetition(Petition):
    """Petition type for academic requests."""

    petition_type: str = "academic"
    receiver: str = "Dean"
    attachment_required: bool = False
