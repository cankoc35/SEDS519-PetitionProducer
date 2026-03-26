"""Singleton petition registry."""

from __future__ import annotations

import json
from pathlib import Path

from models.academic_petition import AcademicPetition
from models.administrative_petition import AdministrativePetition
from models.petition import Petition


class PetitionRegistry:
    """Central registry shared across the application."""

    _instance: "PetitionRegistry | None" = None

    def __new__(cls) -> "PetitionRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._petitions = []
            cls._instance._storage_dir = (
                Path(__file__).resolve().parents[2] / "data" / "petitions"
            )
            cls._instance._storage_dir.mkdir(parents=True, exist_ok=True)
            cls._instance.load_all_petitions()
        return cls._instance

    def add_petition(self, petition: Petition) -> None:
        if petition not in self._petitions:
            self._petitions.append(petition)
        self.save_all_petitions()

    def register_petition(self, petition: Petition) -> None:
        """Mark a petition as registered and keep it in the registry."""
        if petition not in self._petitions:
            self._petitions.append(petition)
        petition.status = "registered"
        self.save_all_petitions()

    def get_all_petitions(self) -> list[Petition]:
        return list(self._petitions)

    def get_draft_petitions(self) -> list[Petition]:
        """Return petitions that are still being written."""
        return [petition for petition in self._petitions if petition.status == "draft"]

    def get_registered_petitions(self) -> list[Petition]:
        """Return petitions that have been registered."""
        return [petition for petition in self._petitions if petition.status == "registered"]

    def save_all_petitions(self) -> None:
        """Persist all petitions as JSON files in the storage folder."""
        for json_file in self._storage_dir.glob("petition_*.json"):
            json_file.unlink()

        for index, petition in enumerate(self._petitions, start=1):
            file_path = self._storage_dir / f"petition_{index}.json"
            with file_path.open("w", encoding="utf-8") as file:
                json.dump(petition.to_dict(), file, indent=2)

    def load_all_petitions(self) -> None:
        """Load petitions from JSON files in the storage folder."""
        self._petitions = []
        for file_path in sorted(self._storage_dir.glob("petition_*.json")):
            with file_path.open("r", encoding="utf-8") as file:
                petition_data = json.load(file)
            self._petitions.append(self._petition_from_dict(petition_data))

    def _petition_from_dict(self, petition_data: dict[str, object]) -> Petition:
        """Rebuild the correct petition object from stored JSON data."""
        common_fields = {
            "title": petition_data["title"],
            "body": petition_data["body"],
            "petitioner": petition_data["petitioner"],
            "created_by": petition_data["created_by"],
            "status": petition_data.get("status", "draft"),
            "attachment_required": petition_data.get("attachment_required", False),
            "attachments": petition_data.get("attachments", []),
        }
        petition_type = petition_data.get("petition_type")

        if petition_type == "academic":
            return AcademicPetition(
                **common_fields,
                petition_type="academic",
                receiver=str(petition_data.get("receiver", "Dean")),
            )
        if petition_type == "administrative":
            return AdministrativePetition(
                **common_fields,
                petition_type="administrative",
                receiver=str(petition_data.get("receiver", "Administrative Office")),
            )
        return Petition(**common_fields)
