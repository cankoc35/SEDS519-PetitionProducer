"""Application entry point."""

from gui.app import PetitionApp


def main() -> None:
    """Launch the desktop GUI."""
    PetitionApp().run()


if __name__ == "__main__":
    main()
