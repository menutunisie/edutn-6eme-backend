import os

from app.db.session import SessionLocal
from app.models.axis import Axis
from app.models.enums import ValidationStatus
from app.models.lesson import Lesson
from app.models.school_level import SchoolLevel
from app.models.subject import Subject
from app.models.term import Term
from app.models.unit import Unit

ADMIN_EMAIL = os.environ["ADMIN_DEFAULT_EMAIL"]
ADMIN_PASSWORD = os.environ["ADMIN_DEFAULT_PASSWORD"]


def _admin_headers(client) -> dict:
    tokens = client.post(
        "/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    ).json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def _seed_unit() -> Unit:
    """Cree School Level -> Subject -> Term -> Unit (sans Axis/Lesson) pour
    servir de base aux tests d'Axis."""
    db = SessionLocal()
    try:
        school_level = SchoolLevel(code="axis-test-level", name_fr="Niveau test", name_ar="مستوى")
        db.add(school_level)
        db.flush()

        subject = Subject(
            school_level_id=school_level.id,
            code="AXIS_TEST_SUBJECT",
            name_fr="Matiere test",
            name_ar="مادة",
            color="#2563EB",
        )
        db.add(subject)
        db.flush()

        term = Term(subject_id=subject.id, code="T1", name_fr="Premier trimestre", name_ar="الثلاثي الأول")
        db.add(term)
        db.flush()

        unit = Unit(term_id=term.id, title_fr="Unite test", status=ValidationStatus.PUBLISHED)
        db.add(unit)
        db.commit()
        db.refresh(unit)
        return unit
    finally:
        db.close()


def test_axis_endpoints_require_authentication(client):
    unit = _seed_unit()
    assert client.get("/admin/axes", params={"unit_id": str(unit.id)}).status_code == 401


def test_admin_can_create_list_and_update_axis(client):
    unit = _seed_unit()
    headers = _admin_headers(client)

    create_response = client.post(
        "/admin/axes",
        json={
            "unit_id": str(unit.id),
            "title_ar": "محور تجريبي",
            "display_order": 1,
            "status": "a_verifier",
        },
        headers=headers,
    )
    assert create_response.status_code == 201
    axis = create_response.json()
    assert axis["unit_id"] == str(unit.id)
    assert axis["title_fr"] is None
    assert axis["title_ar"] == "محور تجريبي"

    list_response = client.get("/admin/axes", params={"unit_id": str(unit.id)}, headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    patch_response = client.patch(
        f"/admin/axes/{axis['id']}",
        json={"status": "publie", "title_fr": "Axe traduit"},
        headers=headers,
    )
    assert patch_response.status_code == 200
    updated = patch_response.json()
    assert updated["status"] == "publie"
    assert updated["title_fr"] == "Axe traduit"
    # title_ar non fourni au PATCH : doit rester inchange (exclude_unset).
    assert updated["title_ar"] == "محور تجريبي"


def test_lessons_are_correctly_linked_to_their_axis(client):
    """Reproduit le cas Eveil scientifique : 2 Axis sous une Unit, chacun
    avec ses propres Lesson, correctement isolees par /admin/lessons."""
    unit = _seed_unit()

    db = SessionLocal()
    try:
        axis_1 = Axis(unit_id=unit.id, title_ar="محور 1", status=ValidationStatus.TO_REVIEW, display_order=1)
        axis_2 = Axis(unit_id=unit.id, title_ar="محور 2", status=ValidationStatus.TO_REVIEW, display_order=2)
        db.add_all([axis_1, axis_2])
        db.flush()

        lesson_1 = Lesson(unit_id=unit.id, axis_id=axis_1.id, title_ar="درس 1أ", status=ValidationStatus.TO_REVIEW)
        lesson_2 = Lesson(unit_id=unit.id, axis_id=axis_1.id, title_ar="درس 1ب", status=ValidationStatus.TO_REVIEW)
        lesson_3 = Lesson(unit_id=unit.id, axis_id=axis_2.id, title_ar="درس 2أ", status=ValidationStatus.TO_REVIEW)
        db.add_all([lesson_1, lesson_2, lesson_3])
        db.commit()

        unit_id = str(unit.id)
        axis_1_id = str(axis_1.id)
        axis_2_id = str(axis_2.id)
    finally:
        db.close()

    headers = _admin_headers(client)

    axes = client.get("/admin/axes", params={"unit_id": unit_id}, headers=headers).json()
    assert {a["id"] for a in axes} == {axis_1_id, axis_2_id}
    assert all(a["unit_id"] == unit_id for a in axes)

    all_lessons = client.get("/admin/lessons", params={"unit_id": unit_id}, headers=headers).json()
    assert len(all_lessons) == 3

    axis_1_lessons = client.get(
        "/admin/lessons", params={"unit_id": unit_id, "axis_id": axis_1_id}, headers=headers
    ).json()
    assert len(axis_1_lessons) == 2
    assert all(l["axis_id"] == axis_1_id for l in axis_1_lessons)

    axis_2_lessons = client.get(
        "/admin/lessons", params={"unit_id": unit_id, "axis_id": axis_2_id}, headers=headers
    ).json()
    assert len(axis_2_lessons) == 1
    assert axis_2_lessons[0]["axis_id"] == axis_2_id


def test_lessons_without_axis_still_work_like_mathematics(client):
    """Les matieres sans niveau Axis (ex. Mathematiques) doivent continuer a
    fonctionner exactement comme avant : Lesson rattachee directement a
    l'Unit, axis_id=None."""
    unit = _seed_unit()

    db = SessionLocal()
    try:
        lesson = Lesson(unit_id=unit.id, title_fr="Lecon sans axe", status=ValidationStatus.TO_REVIEW)
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        unit_id = str(unit.id)
        lesson_id = str(lesson.id)
    finally:
        db.close()

    headers = _admin_headers(client)

    # Aucun Axis sous cette Unit.
    assert client.get("/admin/axes", params={"unit_id": unit_id}, headers=headers).json() == []

    lessons = client.get("/admin/lessons", params={"unit_id": unit_id}, headers=headers).json()
    assert len(lessons) == 1
    assert lessons[0]["id"] == lesson_id
    assert lessons[0]["axis_id"] is None
    assert lessons[0]["title_fr"] == "Lecon sans axe"
