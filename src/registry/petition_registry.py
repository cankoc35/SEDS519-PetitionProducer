"""Singleton petition registry."""

from __future__ import annotations

from models.petition import Petition


class PetitionRegistry:
    """Central registry shared across the application."""

    _instance: "PetitionRegistry | None" = None

    def __new__(cls) -> "PetitionRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._petitions = []
        return cls._instance

    def add_petition(self, petition: Petition) -> None:
        self._petitions.append(petition)

    def get_all_petitions(self) -> list[Petition]:
        return list(self._petitions)
