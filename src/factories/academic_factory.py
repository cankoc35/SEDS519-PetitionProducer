"""Factory for academic petitions."""

from models.academic_petition import AcademicPetition

from .petition_factory import PetitionFactory


class AcademicPetitionFactory(PetitionFactory):
    """Create academic petitions with academic defaults."""

    def create_petition(self, title: str, body: str, petitioner: str) -> AcademicPetition:
        return AcademicPetition(title=title, body=body, petitioner=petitioner)
