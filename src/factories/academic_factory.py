"""Factory for academic petitions."""

from __future__ import annotations

from models.academic_petition import AcademicPetition

from .petition_factory import PetitionFactory


class AcademicPetitionFactory(PetitionFactory):
    """Create academic petitions with academic defaults."""

    def create_petition(
        self,
        title: str,
        body: str,
        petitioner: str,
        created_by: str,
        status: str = "draft",
        attachment_required: bool = False,
        attachments: list[str] | None = None,
    ) -> AcademicPetition:
        return AcademicPetition(
            title=title,
            body=body,
            petitioner=petitioner,
            created_by=created_by,
            status=status,
            attachment_required=attachment_required,
            attachments=attachments or [],
        )
