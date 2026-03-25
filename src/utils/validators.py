"""Validation helpers for petitions."""

from models.petition import Petition


def is_valid_petition(petition: Petition) -> bool:
    """Check the basic validity rules required by the homework."""
    if not petition.body.strip():
        return False
    if petition.attachment_required and not petition.attachments:
        return False
    return True
