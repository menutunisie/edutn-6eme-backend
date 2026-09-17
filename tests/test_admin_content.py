import os

from app.db.session import SessionLocal
from app.models.enums import ValidationStatus
from app.models.school_level import SchoolLevel
from app.models.subject import Subject
from app.models.term import Term
from app.models.unit import Unit
from tests.test_public_content import _seed_minimal_content

ADMIN_EMAIL = os.environ["ADMIN_DEFAULT_EMAIL"]
ADMIN_PASSWORD = os.environ["ADMIN_DEFAULT_PASSWORD"]


def _admin_headers(client) -> dict:
    tokens = client.post(
        "/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    ).json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def test_admin_content_endpoints_require_authentication(client):
    assert client.get("/admin/subjects").status_code == 401


def test_admin_content_endpoints_reject_non_admin(client):
    headers = _admin_headers(client)
    client.post(
        "/admin/users",
        json={
            "email": "teacher.content@edutn6.tn",
            "full_name": "Prof Contenu",
            "password": "ProfDemo123!",
            "role": "TEACHER",
        },
        headers=headers,
    )
    teacher_tokens = client.post(
        "/auth/login", json={"email": "teacher.content@edutn6.tn", "password": "ProfDemo123!"}
    ).json()
    teacher_headers = {"Authorization": f"Bearer {teacher_tokens['access_token']}"}

    assert client.get("/admin/subjects", headers=teacher_headers).status_code == 403


def test_admin_can_walk_the_full_hierarchy(client):
    lesson = _seed_minimal_content(lesson_status=ValidationStatus.TO_REVIEW)
    headers = _admin_headers(client)

    subjects = client.get("/admin/subjects", headers=headers).json()
    assert len(subjects) == 1
    subject_id = subjects[0]["id"]

    terms = client.get("/admin/terms", params={"subject_id": subject_id}, headers=headers).json()
    assert len(terms) == 1
    term_id = terms[0]["id"]

    units = client.get("/admin/units", params={"term_id": term_id}, headers=headers).json()
    assert len(units) == 1
    unit_id = units[0]["id"]
    assert units[0]["status"] == "publie"  # cf. _seed_minimal_content : Unit toujours PUBLISHED

    lessons = client.get("/admin/lessons", params={"unit_id": unit_id}, headers=headers).json()
    assert len(lessons) == 1
    assert lessons[0]["id"] == str(lesson.id)
    assert lessons[0]["status"] == "a_verifier"


def test_admin_lessons_endpoint_exposes_non_published_statuses_unlike_public_endpoint(client):
    lesson = _seed_minimal_content(lesson_status=ValidationStatus.DRAFT)
    headers = _admin_headers(client)

    lessons = client.get(
        "/admin/lessons", params={"unit_id": str(lesson.unit_id)}, headers=headers
    ).json()
    assert len(lessons) == 1
    assert lessons[0]["status"] == "brouillon"

    # Contrairement a /admin/lessons, /public/lessons ne l'expose jamais.
    public_response = client.get("/public/lessons").json()
    assert all(item["id"] != str(lesson.id) for item in public_response)


def test_unit_with_null_title_fr_is_accepted_and_exposed_by_admin_api(client):
    """title_fr est nullable (voir migration 67b1bc6b15ab) : cas reel pour
    les Unit dont seul le titre arabe verifie est disponible pour l'instant
    (ex. les 12 axes maths T1)."""
    db = SessionLocal()
    try:
        school_level = SchoolLevel(
            code="test-null-title-level", name_fr="Niveau test", name_ar="مستوى"
        )
        db.add(school_level)
        db.flush()

        subject = Subject(
            school_level_id=school_level.id,
            code="TEST_NULL_TITLE_SUBJECT",
            name_fr="Matiere test",
            name_ar="مادة",
            color="#2563EB",
        )
        db.add(subject)
        db.flush()

        term = Term(
            subject_id=subject.id, code="T1", name_fr="Premier trimestre", name_ar="الثلاثي الأول"
        )
        db.add(term)
        db.flush()

        # title_fr=None accepte sans erreur d'integrite : c'est le coeur du test.
        unit = Unit(
            term_id=term.id,
            title_fr=None,
            title_ar="عنوان تجريبي بالعربية فقط",
            status=ValidationStatus.TO_REVIEW,
        )
        db.add(unit)
        db.commit()
        db.refresh(unit)
        term_id = str(term.id)
        unit_id = str(unit.id)
    finally:
        db.close()

    headers = _admin_headers(client)
    units = client.get("/admin/units", params={"term_id": term_id}, headers=headers).json()

    assert len(units) == 1
    assert units[0]["id"] == unit_id
    assert units[0]["title_fr"] is None
    assert units[0]["title_ar"] == "عنوان تجريبي بالعربية فقط"
    assert units[0]["status"] == "a_verifier"
