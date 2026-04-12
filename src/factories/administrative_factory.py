"""Factory for administrative petitions."""

from __future__ import annotations

from models.administrative_petition import AdministrativePetition

from .petition_factory import PetitionFactory


class AdministrativePetitionFactory(PetitionFactory):
    """Create administrative petitions with administrative defaults."""

    def create_petition(
        self,
        title: str,
        body: str,
        petitioner: str,
        created_by: str,
        status: str = "draft",
        attachment_required: bool = False,
        attachments: list[str] | None = None,
    ) -> AdministrativePetition:
        return AdministrativePetition(
            title=title,
            body=body,
            petitioner=petitioner,
            created_by=created_by,
            status=status,
            attachment_required=attachment_required,
            attachments=attachments or [],
        )
