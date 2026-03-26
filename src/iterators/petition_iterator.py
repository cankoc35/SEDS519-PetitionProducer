"""Iterator for traversing petitions."""

from __future__ import annotations

from models.petition import Petition


class PetitionIterator:
    """Iterate over petitions with optional type and status filters."""

    def __init__(
        self,
        petitions: list[Petition],
        petition_type: str | None = None,
        status: str | None = None,
    ) -> None:
        self._petitions = petitions
        self._petition_type = petition_type
        self._status = status
        self._index = 0

    def __iter__(self) -> "PetitionIterator":
        return self

    def __next__(self) -> Petition:
        while self._index < len(self._petitions):
            petition = self._petitions[self._index]
            self._index += 1
            matches_type = self._petition_type is None or getattr(
                petition, "petition_type", None
            ) == self._petition_type
            matches_status = self._status is None or petition.status == self._status
            if matches_type and matches_status:
                return petition
        raise StopIteration
