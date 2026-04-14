"""Built-in petition template catalog."""

from factories.academic_factory import AcademicPetitionFactory
from factories.administrative_factory import AdministrativePetitionFactory
from models.petition import Petition


def get_academic_templates() -> list[Petition]:
    """Return the built-in academic petition templates."""
    factory = AcademicPetitionFactory()
    templates = [
        factory.create_petition(
            title="Make-Up Exam Request",
            body=(
                "I respectfully submit this petition to request a make-up examination "
                "for the scheduled assessment that I was unable to attend. On the date "
                "of the exam, I experienced an unavoidable circumstance that prevented "
                "my participation, and therefore I could not complete the examination "
                "together with the rest of the class. I value my academic responsibilities "
                "and I do not wish to lose the opportunity to be evaluated for the course "
                "because of a situation beyond my control. I kindly ask the faculty and "
                "the course instructor to review my case and to grant me permission to "
                "take a make-up exam at an appropriate time determined by the department. "
                "If required, I am prepared to submit any supporting explanation or "
                "documentation related to my absence. I would be grateful for your "
                "understanding and your favorable evaluation of my request."
            ),
            petitioner="[Student Name]",
            created_by="system",
        ),
        factory.create_petition(
            title="Course Exemption Request",
            body=(
                "I respectfully submit this petition to request exemption from the "
                "specified course on the basis of my previous academic background and "
                "prior successful completion of equivalent coursework. During my earlier "
                "studies, I completed a course whose content, learning outcomes, and "
                "credit structure substantially overlap with the course for which I am "
                "seeking exemption. For this reason, I believe that I have already "
                "satisfied the academic requirements intended by the curriculum. I kindly "
                "request that the relevant academic board or department review my previous "
                "transcript, course descriptions, and any additional records that may be "
                "necessary in order to assess equivalency. Granting this exemption would "
                "allow me to continue my academic plan more efficiently while maintaining "
                "the integrity of the program requirements. I respectfully ask for your "
                "consideration and a positive decision regarding this request."
            ),
            petitioner="[Student Name]",
            created_by="system",
        ),
        factory.create_petition(
            title="Internship Approval Request",
            body=(
                "I respectfully submit this petition to request approval for my proposed "
                "internship process and the evaluation of the attached internship "
                "documents. I have identified an internship opportunity that I believe is "
                "relevant to my field of study and consistent with the objectives of my "
                "academic program. The institution where I plan to complete the internship "
                "offers work that will help me develop practical knowledge, professional "
                "skills, and direct experience related to my department. In order to move "
                "forward with the placement, I kindly request that the faculty review the "
                "attached company information, internship details, and any supporting "
                "documents required by the department. I am ready to comply with all "
                "institutional procedures, deadlines, and documentation rules connected "
                "to the internship process. I would appreciate your review of my "
                "application and your approval so that I may proceed with the internship "
                "in accordance with university regulations."
            ),
            petitioner="[Student Name]",
            created_by="system",
            attachment_required=True,
        ),
    ]
    return templates


def get_administrative_templates() -> list[Petition]:
    """Return the built-in administrative petition templates."""
    factory = AdministrativePetitionFactory()
    return [
        factory.create_petition(
            title="Student ID Renewal Request",
            body=(
                "I respectfully submit this petition to request the renewal of my student "
                "identification card. My current student ID card has either expired, been "
                "damaged, or become unusable for daily academic and administrative needs. "
                "As the identification card is required for accessing campus facilities, "
                "verifying student status, and benefiting from student services, I kindly "
                "ask the administrative office to process a renewal at the earliest "
                "possible opportunity. I understand that there may be certain procedures, "
                "verification steps, or fees associated with the renewal process, and I am "
                "prepared to fulfill all necessary requirements. I would be grateful if my "
                "application could be reviewed and the renewed card issued so that I may "
                "continue to use university resources without interruption. Thank you for "
                "your time, attention, and support regarding this administrative request."
            ),
            petitioner="[Student Name]",
            created_by="system",
        ),
        factory.create_petition(
            title="Official Document Request",
            body=(
                "I respectfully submit this petition to request the preparation and "
                "delivery of the official document indicated in this application. I need "
                "the requested document for an official purpose, and I kindly ask the "
                "administrative office to review my request and issue the document in "
                "accordance with institutional procedures. The document may be required "
                "for academic, administrative, legal, scholarship, internship, or other "
                "formal processes, and receiving it within the appropriate timeframe would "
                "be of significant importance to me. If additional identification, form "
                "completion, or verification is necessary, I am fully prepared to provide "
                "the relevant information promptly. I would appreciate your assistance in "
                "preparing the requested record accurately and making it available through "
                "the proper delivery method. Thank you in advance for your consideration "
                "and for your support in handling this request."
            ),
            petitioner="[Student Name]",
            created_by="system",
        ),
        factory.create_petition(
            title="Dormitory Issue Request",
            body=(
                "I respectfully submit this petition regarding a dormitory-related issue "
                "that requires administrative review and assistance. During my stay in the "
                "dormitory, I have experienced a situation that has negatively affected my "
                "living conditions, comfort, or ability to continue my daily routine in a "
                "healthy and safe environment. I kindly ask the responsible administrative "
                "unit to examine the matter described in this petition and to take the "
                "necessary action within the framework of dormitory regulations. I believe "
                "that resolving this issue promptly would contribute positively to the "
                "well-being of both myself and other students who may be affected by "
                "similar conditions. If needed, I am ready to provide additional details, "
                "clarifications, or supporting information to assist in the review process. "
                "Thank you for your time and for your attention to this matter. I "
                "respectfully request your support and a suitable solution."
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
