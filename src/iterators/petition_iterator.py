"""Iterator for traversing petitions."""

from __future__ import annotations

from models.petition import Petition


class PetitionIterator:
    """Iterate over petitions with an optional status filter."""

    def __init__(self, petitions: list[Petition], status: str | None = None) -> None:
        self._petitions = petitions
        self._status = status
        self._index = 0

    def __iter__(self) -> "PetitionIterator":
        return self

    def __next__(self) -> Petition:
        while self._index < len(self._petitions):
            petition = self._petitions[self._index]
            self._index += 1
            if self._status is None or petition.status == self._status:
                return petition
        raise StopIteration
