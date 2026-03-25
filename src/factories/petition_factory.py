"""Factory Method base type for petition creation."""

from __future__ import annotations

from abc import ABC, abstractmethod

from models.petition import Petition


class PetitionFactory(ABC):
    """Base class for concrete petition factories."""

    @abstractmethod
    def create_petition(self, title: str, body: str, petitioner: str) -> Petition:
        """Create and return a petition object."""
        raise NotImplementedError
