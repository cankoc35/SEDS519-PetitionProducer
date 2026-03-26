"""GUI form definitions for petition creation and display."""

from __future__ import annotations

import flet as ft

from models.petition import Petition


def build_template_section(
    title: str,
    icon: str,
    templates: list[Petition],
    on_select: ft.ControlEventHandler[ft.ListTile],
) -> ft.Card:
    """Build a card that displays petition templates for one category."""
    return ft.Card(
        elevation=1,
        content=ft.Container(
            padding=20,
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Icon(icon, size=22),
                            ft.Text(title, size=22, weight=ft.FontWeight.W_600),
                        ],
                    ),
                    ft.Text(
                        "Choose a built-in template to start editing a petition.",
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Column(
                        spacing=8,
                        controls=[
                            ft.ListTile(
                                adaptive=True,
                                leading=ft.Icon(ft.Icons.DESCRIPTION_OUTLINED),
                                title=ft.Text(template.title),
                                subtitle=ft.Text(
                                    f"Receiver: {getattr(template, 'receiver', '-')}"
                                ),
                                trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                                data=template,
                                on_click=on_select,
                                bgcolor=ft.Colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=12),
                            )
                            for template in templates
                        ],
                    ),
                ],
            ),
        ),
    )
