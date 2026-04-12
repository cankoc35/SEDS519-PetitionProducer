"""Main GUI application module."""

from __future__ import annotations

from pathlib import Path

import flet as ft

from factories.academic_factory import AcademicPetitionFactory
from factories.administrative_factory import AdministrativePetitionFactory
from iterators.petition_iterator import PetitionIterator
from registry.petition_registry import PetitionRegistry
from registry.template_registry import TemplateRegistry
from templates.petition_templates import get_template_catalog
from utils.validators import is_valid_petition

from .forms import build_saved_petitions_section, build_template_section


class PetitionApp:
    """Top-level GUI application."""

    def run(self) -> None:
        """Start the Flet desktop application."""
        ft.app(target=self.main)

    def main(self, page: ft.Page) -> None:
        """Configure and render petition views."""
        registry = PetitionRegistry()
        template_registry = TemplateRegistry()
        built_in_template_catalog = get_template_catalog()
        current_petition: dict[str, object | None] = {"value": None}
        current_template_title: dict[str, str] = {"value": "No template selected."}

        page.title = "Petition Producer"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.bgcolor = ft.Colors.BLUE_GREY_50
        page.window.width = 1180
        page.window.height = 760
        page.window.min_width = 900
        page.window.min_height = 640

        def show_snack(message: str) -> None:
            page.open(ft.SnackBar(ft.Text(message)))

        title_field = ft.TextField(label="Title")
        body_field = ft.TextField(
            label="Body",
            multiline=True,
            min_lines=8,
            max_lines=12,
        )
        petitioner_field = ft.TextField(label="Petitioner Name")
        receiver_field = ft.TextField(label="Receiver")
        created_by_field = ft.TextField(label="Created By / Username")
        attachments_label = ft.Text("No attachments selected.")
        attachment_requirement_text = ft.Text(
            "",
            color=ft.Colors.RED_700,
            weight=ft.FontWeight.W_600,
        )

        def sync_form_to_petition() -> object | None:
            petition = current_petition["value"]
            if petition is None:
                return None
            petition.title = title_field.value or ""
            petition.body = body_field.value or ""
            petition.petitioner = petitioner_field.value or ""
            petition.receiver = receiver_field.value or ""
            petition.created_by = created_by_field.value or ""
            return petition

        def clear_editor() -> None:
            current_petition["value"] = None
            current_template_title["value"] = "No template selected."
            title_field.value = ""
            body_field.value = ""
            petitioner_field.value = ""
            receiver_field.value = ""
            created_by_field.value = ""
            attachments_label.value = "No attachments selected."
            attachment_requirement_text.value = ""

        def handle_files_picked(event: ft.FilePickerResultEvent) -> None:
            petition = current_petition["value"]
            if petition is None:
                return

            selected_files = event.files or []
            petition.attachments = [
                getattr(file, "path", None) or getattr(file, "name", "")
                for file in selected_files
            ]
            file_names = [getattr(file, "name", "attachment") for file in selected_files]
            attachments_label.value = (
                ", ".join(file_names) if file_names else "No attachments selected."
            )
            page.update()

        file_picker = ft.FilePicker(on_result=handle_files_picked)
        page.overlay.append(file_picker)

        def pick_attachments(_: ft.ControlEvent) -> None:
            if current_petition["value"] is None:
                show_snack("Please start a petition first.")
                return
            show_snack("Opening file picker...")
            file_picker.pick_files(
                dialog_title="Select petition attachments",
                allow_multiple=True,
            )

        def save_current_template(_: ft.ControlEvent | None = None) -> None:
            petition = sync_form_to_petition()
            if petition is None:
                show_snack("Please start a petition first.")
                return
            if not petition.title.strip():
                show_snack("Template title is required.")
                return

            template = petition.clone()
            template.status = "draft"
            template_registry.add_template(template)
            show_snack(f'"{template.title}" was saved as a reusable template.')
            render_route()

        def save_current_petition(status: str) -> None:
            petition = sync_form_to_petition()
            if petition is None:
                show_snack("Please start a petition first.")
                return
            if not petition.petitioner.strip() or not petition.created_by.strip():
                show_snack("Petitioner name and username are required.")
                return
            if not is_valid_petition(petition):
                show_snack("Petition body cannot be empty. Add attachments if required.")
                return

            if status == "registered":
                registry.register_petition(petition)
                show_snack(f'"{petition.title}" was registered successfully.')
            else:
                petition.status = "draft"
                registry.add_petition(petition)
                show_snack(f'"{petition.title}" was saved as draft.')

            clear_editor()
            page.go("/")

        def open_editor_for_petition(petition: object, source_title: str) -> None:
            current_petition["value"] = petition
            current_template_title["value"] = source_title
            title_field.value = petition.title
            body_field.value = petition.body
            petitioner_field.value = petition.petitioner
            receiver_field.value = getattr(petition, "receiver", "")
            created_by_field.value = petition.created_by
            attachments_label.value = (
                ", ".join(petition.attachments)
                if petition.attachments
                else "No attachments selected."
            )
            attachment_requirement_text.value = (
                "Attachments are required for this petition."
                if getattr(petition, "attachment_required", False)
                else ""
            )
            page.go("/edit")

        def start_template_edit(event: ft.ControlEvent) -> None:
            template = getattr(event.control, "data", None)
            if template is None:
                show_snack("Template selection failed. Please try again.")
                return

            petition = template.clone()
            petition.status = "draft"
            if petition.petitioner == "[Student Name]":
                petition.petitioner = ""
            if petition.created_by == "system":
                petition.created_by = ""

            open_editor_for_petition(petition, template.title)

        def start_blank_petition(petition_type: str) -> None:
            if petition_type == "academic":
                petition = AcademicPetitionFactory().create_petition(
                    title="",
                    body="",
                    petitioner="",
                    created_by="",
                )
                source_title = "Blank Academic Petition"
            else:
                petition = AdministrativePetitionFactory().create_petition(
                    title="",
                    body="",
                    petitioner="",
                    created_by="",
                )
                source_title = "Blank Administrative Petition"

            petition.status = "draft"
            open_editor_for_petition(petition, source_title)

        def build_saved_petition_tile(petition: object) -> ft.ListTile:
            petition_type = getattr(petition, "petition_type", "petition").title()
            receiver = getattr(petition, "receiver", "-")
            attachment_names = [
                Path(str(attachment)).name for attachment in getattr(petition, "attachments", [])
            ]
            attachment_summary = (
                ", ".join(attachment_names[:2])
                + (" ..." if len(attachment_names) > 2 else "")
                if attachment_names
                else "No attachments"
            )
            subtitle = (
                f"Type: {petition_type} | Status: {petition.status} | "
                f"Petitioner: {petition.petitioner or '-'} | Receiver: {receiver} | "
                f"Attachments: {attachment_summary}"
            )
            return ft.ListTile(
                adaptive=True,
                leading=ft.Icon(ft.Icons.DESCRIPTION_ROUNDED),
                title=ft.Text(petition.title),
                subtitle=ft.Text(subtitle),
                trailing=ft.Text(
                    petition.status.title(),
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.BLUE_GREY_700,
                ),
                bgcolor=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=12),
            )

        type_filter = ft.Dropdown(
            label="Type Filter",
            width=220,
            value="all",
            options=[
                ft.dropdown.Option("all", "All Types"),
                ft.dropdown.Option("academic", "Academic"),
                ft.dropdown.Option("administrative", "Administrative"),
            ],
        )
        status_filter = ft.Dropdown(
            label="Status Filter",
            width=220,
            value="all",
            options=[
                ft.dropdown.Option("all", "All Statuses"),
                ft.dropdown.Option("draft", "Draft"),
                ft.dropdown.Option("registered", "Registered"),
            ],
        )

        def build_saved_petitions_content() -> ft.Column:
            petition_type = None if type_filter.value == "all" else type_filter.value
            status = None if status_filter.value == "all" else status_filter.value
            petitions = list(
                PetitionIterator(
                    registry.get_all_petitions(),
                    petition_type=petition_type,
                    status=status,
                )
            )
            if petitions:
                controls = [build_saved_petition_tile(petition) for petition in petitions]
            else:
                controls = [
                    ft.Container(
                        bgcolor=ft.Colors.WHITE,
                        border_radius=12,
                        padding=16,
                        content=ft.Text("No saved petitions yet."),
                    )
                ]
            return ft.Column(spacing=8, controls=controls)

        def render_route(_: ft.RouteChangeEvent | None = None) -> None:
            user_templates = template_registry.get_all_templates()
            saved_count_text = ft.Text(
                f"{len(registry.get_all_petitions())} saved petitions",
                weight=ft.FontWeight.W_600,
            )
            built_in_template_count_text = ft.Text(
                f"{sum(len(items) for items in built_in_template_catalog.values())} built-in templates",
                weight=ft.FontWeight.W_600,
            )
            user_template_count_text = ft.Text(
                f"{len(user_templates)} user templates",
                weight=ft.FontWeight.W_600,
            )

            page.views.clear()

            main_header = ft.Container(
                padding=24,
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text("Petition Producer", size=32, weight=ft.FontWeight.W_700),
                        ft.Text(
                            "Choose a template, clone a saved one, or start a new petition from scratch.",
                            size=16,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                        ft.Row(
                            spacing=12,
                            controls=[
                                ft.Container(
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=16,
                                    padding=ft.padding.symmetric(horizontal=14, vertical=10),
                                    content=built_in_template_count_text,
                                ),
                                ft.Container(
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=16,
                                    padding=ft.padding.symmetric(horizontal=14, vertical=10),
                                    content=user_template_count_text,
                                ),
                                ft.Container(
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=16,
                                    padding=ft.padding.symmetric(horizontal=14, vertical=10),
                                    content=saved_count_text,
                                ),
                            ],
                        ),
                    ],
                ),
            )

            quick_start_section = ft.Card(
                elevation=1,
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Row(
                                spacing=10,
                                controls=[
                                    ft.Icon(ft.Icons.AUTO_AWESOME_OUTLINED, size=22),
                                    ft.Text(
                                        "Start From Scratch",
                                        size=22,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                ],
                            ),
                            ft.Text(
                                "Create a blank academic or administrative petition, then optionally save it as your own reusable template.",
                                color=ft.Colors.ON_SURFACE_VARIANT,
                            ),
                            ft.Row(
                                wrap=True,
                                spacing=12,
                                controls=[
                                    ft.ElevatedButton(
                                        "New Academic Petition",
                                        icon=ft.Icons.SCHOOL_OUTLINED,
                                        on_click=lambda _: start_blank_petition("academic"),
                                    ),
                                    ft.ElevatedButton(
                                        "New Administrative Petition",
                                        icon=ft.Icons.BUSINESS_CENTER_OUTLINED,
                                        on_click=lambda _: start_blank_petition("administrative"),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            )

            template_layout = ft.ResponsiveRow(
                columns=12,
                run_spacing=16,
                controls=[
                    ft.Column(
                        col={"xs": 12, "md": 4},
                        controls=[
                            build_template_section(
                                "Academic Templates",
                                ft.Icons.SCHOOL_OUTLINED,
                                built_in_template_catalog["academic"],
                                start_template_edit,
                            )
                        ],
                    ),
                    ft.Column(
                        col={"xs": 12, "md": 4},
                        controls=[
                            build_template_section(
                                "Administrative Templates",
                                ft.Icons.BUSINESS_CENTER_OUTLINED,
                                built_in_template_catalog["administrative"],
                                start_template_edit,
                            )
                        ],
                    ),
                    ft.Column(
                        col={"xs": 12, "md": 4},
                        controls=[
                            build_template_section(
                                "My Templates",
                                ft.Icons.BOOKMARKS_OUTLINED,
                                user_templates,
                                start_template_edit,
                                description="Choose one of your saved custom templates and clone it into a new petition.",
                                empty_message="No user-defined templates yet. Save one from the editor to see it here.",
                            )
                        ],
                    ),
                ],
            )

            saved_petitions_section = build_saved_petitions_section(
                ft.Column(
                    spacing=12,
                    controls=[
                        ft.Row(
                            wrap=True,
                            spacing=12,
                            controls=[type_filter, status_filter],
                        ),
                        build_saved_petitions_content(),
                    ],
                )
            )

            page.views.append(
                ft.View(
                    route="/",
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        main_header,
                        ft.Container(
                            padding=ft.padding.symmetric(horizontal=24),
                            content=quick_start_section,
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(horizontal=24),
                            content=template_layout,
                        ),
                        ft.Container(
                            padding=24,
                            content=saved_petitions_section,
                        ),
                    ],
                )
            )

            if page.route == "/edit":
                page.views.append(
                    ft.View(
                        route="/edit",
                        bgcolor=ft.Colors.BLUE_GREY_50,
                        scroll=ft.ScrollMode.AUTO,
                        appbar=ft.AppBar(
                            leading=ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                on_click=lambda _: page.go("/"),
                            ),
                            title=ft.Text("Petition Editor"),
                            bgcolor=ft.Colors.WHITE,
                        ),
                        controls=[
                            ft.Container(
                                padding=24,
                                content=ft.Column(
                                    spacing=16,
                                    controls=[
                                        ft.Text(
                                            f"Editing Template: {current_template_title['value']}",
                                            size=28,
                                            weight=ft.FontWeight.W_700,
                                        ),
                                        ft.Text(
                                            "Edit the petition, then save it as draft, register it, or store it as a reusable template.",
                                            color=ft.Colors.ON_SURFACE_VARIANT,
                                        ),
                                        ft.Card(
                                            elevation=1,
                                            content=ft.Container(
                                                padding=20,
                                                content=ft.Column(
                                                    spacing=12,
                                                    controls=[
                                                        title_field,
                                                        body_field,
                                                        petitioner_field,
                                                        receiver_field,
                                                        created_by_field,
                                                        ft.Row(
                                                            wrap=True,
                                                            spacing=12,
                                                            controls=[
                                                                ft.ElevatedButton(
                                                                    "Choose Files",
                                                                    icon=ft.Icons.UPLOAD_FILE,
                                                                    on_click=pick_attachments,
                                                                ),
                                                                ft.TextButton(
                                                                    "Cancel",
                                                                    on_click=lambda _: page.go("/"),
                                                                ),
                                                            ],
                                                        ),
                                                        attachments_label,
                                                        attachment_requirement_text,
                                                        ft.Row(
                                                            wrap=True,
                                                            spacing=12,
                                                            controls=[
                                                                ft.ElevatedButton(
                                                                    "Save as Template",
                                                                    icon=ft.Icons.BOOKMARK_ADD_OUTLINED,
                                                                    on_click=save_current_template,
                                                                ),
                                                                ft.ElevatedButton(
                                                                    "Save Draft",
                                                                    on_click=lambda _: save_current_petition("draft"),
                                                                ),
                                                                ft.ElevatedButton(
                                                                    "Register",
                                                                    on_click=lambda _: save_current_petition("registered"),
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                            )
                        ],
                    )
                )

            page.update()

        type_filter.on_change = render_route
        status_filter.on_change = render_route
        page.on_route_change = render_route
        page.go("/")
