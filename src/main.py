"""Application entry point."""

from factories.academic_factory import AcademicPetitionFactory
from factories.administrative_factory import AdministrativePetitionFactory
from iterators.petition_iterator import PetitionIterator
from registry.petition_registry import PetitionRegistry
from utils.validators import is_valid_petition


def print_petitions(title: str, iterator: PetitionIterator) -> None:
    """Print petitions returned by the iterator."""
    print(f"\n{title}")
    for petition in iterator:
        petition_type = getattr(petition, "petition_type", "unknown")
        receiver = getattr(petition, "receiver", "unknown")
        print(
            f"- [{petition.status}] {petition.title} "
            f"({petition_type}, receiver: {receiver}, created_by: {petition.created_by})"
        )


def seed_demo_data(registry: PetitionRegistry) -> None:
    """Create a small initial dataset when no saved petitions exist yet."""
    academic_factory = AcademicPetitionFactory()
    administrative_factory = AdministrativePetitionFactory()

    academic_petition = academic_factory.create_petition(
        title="Make-Up Exam Request",
        body="I request a make-up exam because I missed the midterm due to illness.",
        petitioner="Ayse Yilmaz",
        created_by="ayse",
        attachments=["medical_report.pdf"],
    )
    administrative_petition = administrative_factory.create_petition(
        title="Student ID Renewal Request",
        body="I request the renewal of my student ID card.",
        petitioner="Mehmet Demir",
        created_by="mehmet",
    )

    for petition in [academic_petition, administrative_petition]:
        print(f"{petition.title} valid: {is_valid_petition(petition)}")
        registry.add_petition(petition)

    registry.register_petition(administrative_petition)

    cloned_petition = academic_petition.clone()
    cloned_petition.title = "Course Exemption Request"
    cloned_petition.body = "I request exemption from the introductory programming course."
    cloned_petition.status = "draft"
    registry.add_petition(cloned_petition)


def main() -> None:
    """Run a small non-GUI demonstration of the homework requirements."""
    registry = PetitionRegistry()

    if not registry.get_all_petitions():
        print("No saved petitions found. Creating demo data...")
        seed_demo_data(registry)
    else:
        print(f"Loaded {len(registry.get_all_petitions())} saved petition(s) from JSON storage.")

    all_petitions = registry.get_all_petitions()
    print_petitions("All petitions", PetitionIterator(all_petitions))
    print_petitions(
        "Academic petitions",
        PetitionIterator(all_petitions, petition_type="academic"),
    )
    print_petitions(
        "Registered petitions",
        PetitionIterator(all_petitions, status="registered"),
    )


if __name__ == "__main__":
    main()
