"""Main GUI application module."""

from __future__ import annotations

import flet as ft

from iterators.petition_iterator import PetitionIterator
from registry.petition_registry import PetitionRegistry
from templates.petition_templates import get_template_catalog
from utils.validators import is_valid_petition

from .forms import build_saved_petitions_section, build_template_section


class PetitionApp:
    """Top-level GUI application."""

    def run(self) -> None:
        """Start the Flet desktop application."""
        ft.app(target=self.main)

    def main(self, page: ft.Page) -> None:
        """Configure and render the first petition template screen."""
        registry = PetitionRegistry()
        template_catalog = get_template_catalog()
        attachment_state: dict[str, object | None] = {"petition": None, "label": None}

        page.title = "Petition Producer"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 24
        page.scroll = ft.ScrollMode.AUTO
        page.bgcolor = ft.Colors.BLUE_GREY_50
        page.window.width = 1180
        page.window.height = 760
        page.window.min_width = 900
        page.window.min_height = 640

        def show_snack(message: str) -> None:
            snack_bar = ft.SnackBar(ft.Text(message))
            page.open(snack_bar)

        def build_saved_petition_tile(petition: object) -> ft.ListTile:
            petition_type = getattr(petition, "petition_type", "petition").title()
            receiver = getattr(petition, "receiver", "-")
            subtitle = (
                f"Type: {petition_type} | Status: {petition.status} | "
                f"Petitioner: {petition.petitioner or '-'} | Receiver: {receiver}"
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

        saved_petitions_column = ft.Column(spacing=8)
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

        def refresh_saved_petitions_list() -> None:
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
                saved_petitions_column.controls = [
                    build_saved_petition_tile(petition) for petition in petitions
                ]
            else:
                saved_petitions_column.controls = [
                    ft.Container(
                        bgcolor=ft.Colors.WHITE,
                        border_radius=12,
                        padding=16,
                        content=ft.Text("No saved petitions yet."),
                    )
                ]
            page.update()

        def refresh_saved_count() -> None:
            saved_count_text.value = f"{len(registry.get_all_petitions())} saved petitions"

        def close_dialog(dialog: ft.AlertDialog) -> None:
            page.close(dialog)

        def handle_files_picked(event: ft.FilePickerResultEvent) -> None:
            petition = attachment_state["petition"]
            label = attachment_state["label"]
            if petition is None or label is None:
                return

            selected_files = event.files or []
            petition.attachments = [
                getattr(file, "path", None) or getattr(file, "name", "")
                for file in selected_files
            ]
            file_names = [getattr(file, "name", "attachment") for file in selected_files]
            label.value = (
                ", ".join(file_names) if file_names else "No attachments selected."
            )
            page.update()

        file_picker = ft.FilePicker(on_result=handle_files_picked)
        page.overlay.append(file_picker)

        def open_template_editor(event: ft.ControlEvent) -> None:
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

            title_field = ft.TextField(label="Title", value=petition.title)
            body_field = ft.TextField(
                label="Body",
                value=petition.body,
                multiline=True,
                min_lines=6,
                max_lines=10,
            )
            petitioner_field = ft.TextField(
                label="Petitioner Name",
                value=petition.petitioner,
            )
            receiver_field = ft.TextField(
                label="Receiver",
                value=getattr(petition, "receiver", ""),
            )
            created_by_field = ft.TextField(
                label="Created By / Username",
                value=petition.created_by,
            )
            attachments_label = ft.Text(
                ", ".join(petition.attachments) if petition.attachments else "No attachments selected."
            )

            def sync_form_to_petition() -> None:
                petition.title = title_field.value or ""
                petition.body = body_field.value or ""
                petition.petitioner = petitioner_field.value or ""
                petition.receiver = receiver_field.value or ""
                petition.created_by = created_by_field.value or ""

            def save_petition(status: str) -> None:
                sync_form_to_petition()
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

                refresh_saved_count()
                refresh_saved_petitions_list()
                close_dialog(dialog)

            def pick_attachments(_: ft.ControlEvent) -> None:
                attachment_state["petition"] = petition
                attachment_state["label"] = attachments_label
                file_picker.pick_files(
                    dialog_title="Select petition attachments",
                    allow_multiple=True,
                )

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"Edit Template: {template.title}"),
                content=ft.Container(
                    width=640,
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Text(
                                "The selected template was cloned. Edit the fields below before saving.",
                                color=ft.Colors.ON_SURFACE_VARIANT,
                            ),
                            title_field,
                            body_field,
                            petitioner_field,
                            receiver_field,
                            created_by_field,
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        "Attachments are optional unless the petition requires them."
                                    ),
                                    ft.ElevatedButton(
                                        "Choose Files",
                                        icon=ft.Icons.UPLOAD_FILE,
                                        on_click=pick_attachments,
                                    ),
                                ],
                            ),
                            attachments_label,
                        ],
                    ),
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=lambda _: close_dialog(dialog)),
                    ft.ElevatedButton(
                        "Save Draft",
                        on_click=lambda _: save_petition("draft"),
                    ),
                    ft.ElevatedButton(
                        "Register",
                        on_click=lambda _: save_petition("registered"),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            page.open(dialog)

        saved_count_text = ft.Text(
            f"{len(registry.get_all_petitions())} saved petitions",
            weight=ft.FontWeight.W_600,
        )
        type_filter.on_change = lambda _: refresh_saved_petitions_list()
        status_filter.on_change = lambda _: refresh_saved_petitions_list()
        refresh_saved_petitions_list()

        header = ft.Container(
            padding=ft.padding.only(bottom=16),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text("Petition Producer", size=32, weight=ft.FontWeight.W_700),
                    ft.Text(
                        "Choose one of the built-in academic or administrative petition templates.",
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
                                content=ft.Text(
                                    f"{sum(len(items) for items in template_catalog.values())} templates",
                                    weight=ft.FontWeight.W_600,
                                ),
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

        template_layout = ft.ResponsiveRow(
            columns=12,
            run_spacing=16,
            controls=[
                ft.Column(
                    col={"xs": 12, "md": 6},
                    controls=[
                        build_template_section(
                            "Academic Templates",
                            ft.Icons.SCHOOL_OUTLINED,
                            template_catalog["academic"],
                            open_template_editor,
                        )
                    ],
                ),
                ft.Column(
                    col={"xs": 12, "md": 6},
                    controls=[
                        build_template_section(
                            "Administrative Templates",
                            ft.Icons.BUSINESS_CENTER_OUTLINED,
                            template_catalog["administrative"],
                            open_template_editor,
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
                    saved_petitions_column,
                ],
            )
        )

        page.add(header, template_layout, saved_petitions_section)
