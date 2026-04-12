"""Registry for user-defined petition templates."""

from __future__ import annotations

import json
from pathlib import Path

from models.academic_petition import AcademicPetition
from models.administrative_petition import AdministrativePetition
from models.petition import Petition


class TemplateRegistry:
    """Persist and retrieve user-created petition templates."""

    def __init__(self) -> None:
        self._templates: list[Petition] = []
        self._storage_dir = Path(__file__).resolve().parents[2] / "data" / "templates"
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        self.load_all_templates()

    def add_template(self, template: Petition) -> None:
        """Store a new reusable template and persist it."""
        self._templates.append(template)
        self.save_all_templates()

    def get_all_templates(self) -> list[Petition]:
        """Return all user-defined templates."""
        return list(self._templates)

    def save_all_templates(self) -> None:
        """Persist templates as JSON files in the template storage folder."""
        for json_file in self._storage_dir.glob("template_*.json"):
            json_file.unlink()

        for index, template in enumerate(self._templates, start=1):
            file_path = self._storage_dir / f"template_{index}.json"
            with file_path.open("w", encoding="utf-8") as file:
                json.dump(template.to_dict(), file, indent=2)

    def load_all_templates(self) -> None:
        """Load all user-defined templates from JSON storage."""
        self._templates = []
        for file_path in sorted(self._storage_dir.glob("template_*.json")):
            with file_path.open("r", encoding="utf-8") as file:
                petition_data = json.load(file)
            self._templates.append(self._petition_from_dict(petition_data))

    def _petition_from_dict(self, petition_data: dict[str, object]) -> Petition:
        """Rebuild the correct template subclass from stored JSON data."""
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
