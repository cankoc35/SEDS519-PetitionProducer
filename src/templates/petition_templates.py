"""Built-in petition template catalog."""

from factories.academic_factory import AcademicPetitionFactory
from factories.administrative_factory import AdministrativePetitionFactory
from models.petition import Petition


def get_academic_templates() -> list[Petition]:
    """Return the built-in academic petition templates."""
    factory = AcademicPetitionFactory()
    return [
        factory.create_petition(
            title="Make-Up Exam Request",
            body=(
                "I respectfully request a make-up exam because I was unable to attend "
                "the scheduled exam."
            ),
            petitioner="[Student Name]",
            created_by="system",
        ),
        factory.create_petition(
            title="Course Exemption Request",
            body=(
                "I respectfully request exemption from the specified course based on "
                "my previous academic background."
            ),
            petitioner="[Student Name]",
            created_by="system",
        ),
        factory.create_petition(
            title="Internship Approval Request",
            body=(
                "I respectfully request approval for my internship process and the "
                "evaluation of the attached internship information."
            ),
            petitioner="[Student Name]",
            created_by="system",
        ),
    ]


def get_administrative_templates() -> list[Petition]:
    """Return the built-in administrative petition templates."""
    factory = AdministrativePetitionFactory()
    return [
        factory.create_petition(
            title="Student ID Renewal Request",
            body=(
                "I respectfully request the renewal of my student identification card."
            ),
            petitioner="[Student Name]",
            created_by="system",
        ),
        factory.create_petition(
            title="Official Document Request",
            body=(
                "I respectfully request the preparation and delivery of the official "
                "document stated in this petition."
            ),
            petitioner="[Student Name]",
            created_by="system",
        ),
        factory.create_petition(
            title="Dormitory Issue Request",
            body=(
                "I respectfully submit my request regarding the dormitory-related issue "
                "explained below."
            ),
            petitioner="[Student Name]",
            created_by="system",
        ),
    ]


def get_all_templates() -> list[Petition]:
    """Return all built-in petition templates."""
    return get_academic_templates() + get_administrative_templates()


def get_template_catalog() -> dict[str, list[Petition]]:
    """Return templates grouped by petition type."""
    return {
        "academic": get_academic_templates(),
        "administrative": get_administrative_templates(),
    }
