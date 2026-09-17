import os

from app.models.enums import ValidationStatus
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
