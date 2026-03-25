"""Factory for administrative petitions."""

from models.administrative_petition import AdministrativePetition

from .petition_factory import PetitionFactory


class AdministrativePetitionFactory(PetitionFactory):
    """Create administrative petitions with administrative defaults."""

    def create_petition(self, title: str, body: str, petitioner: str) -> AdministrativePetition:
        return AdministrativePetition(title=title, body=body, petitioner=petitioner)
