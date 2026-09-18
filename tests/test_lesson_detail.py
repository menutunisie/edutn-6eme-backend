import os
import uuid

from app.db.session import SessionLocal
from app.models.enums import ValidationStatus
from app.models.lesson import Lesson
from app.models.school_level import SchoolLevel
from app.models.subject import Subject
from app.models.term import Term
from app.models.unit import Unit

ADMIN_EMAIL = os.environ["ADMIN_DEFAULT_EMAIL"]
ADMIN_PASSWORD = os.environ["ADMIN_DEFAULT_PASSWORD"]

SAMPLE_SECTIONS = [
    {
        "order": 1,
        "phase_key": "observation",
        "title_ar": "ألاحظ",
        "title_fr": None,
        "body_ar": "نص تجريبي",
        "body_fr": None,
        "media_note": "Schéma non numérisé, page 3.",
    },
    {
        "order": 2,
        "phase_key": "conclusion",
        "title_ar": "أستنتج",
        "title_fr": None,
        "body_ar": "نص تجريبي آخر",
        "body_fr": None,
        "media_note": None,
    },
]

# Reproduit la forme de la 2e leçon pilote (العين والرّؤية, 8 phases, dont
# certaines sans media_note) sans dupliquer le texte reel du manuel ici.
SAMPLE_SECTIONS_SECOND_LESSON = [
    {
        "order": i,
        "phase_key": phase_key,
        "title_ar": f"عنوان تجريبي {i}",
        "title_fr": None,
        "body_ar": f"نص تجريبي للمرحلة {i}",
        "body_fr": None,
        "media_note": "Schéma non numérisé." if i in (4, 6) else None,
    }
    for i, phase_key in enumerate(
        [
            "mobilisation_acquis",
            "observation",
            "hypothese",
            "experimentation",
            "conclusion",
            "application",
            "evaluation",
            "vocabulaire",
        ],
        start=1,
    )
]


def _admin_headers(client) -> dict:
    tokens = client.post(
        "/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    ).json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def _seed_lesson(
    *, status: ValidationStatus, content_sections: list | None, title_ar: str = "درس تجريبي"
) -> Lesson:
    db = SessionLocal()
    try:
        school_level = SchoolLevel(
            code=f"detail-test-level-{uuid.uuid4()}", name_fr="Niveau test", name_ar="مستوى"
        )
        db.add(school_level)
        db.flush()

        subject = Subject(
            school_level_id=school_level.id,
            code=f"DETAIL_TEST_{uuid.uuid4()}",
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
        db.flush()

        lesson = Lesson(
            unit_id=unit.id,
            title_ar=title_ar,
            status=status,
            content_sections=content_sections,
        )
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson
    finally:
        db.close()


def test_admin_lesson_detail_includes_content_sections(client):
    lesson = _seed_lesson(status=ValidationStatus.TO_REVIEW, content_sections=SAMPLE_SECTIONS)
    headers = _admin_headers(client)

    response = client.get(f"/admin/lessons/{lesson.id}", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert len(body["content_sections"]) == 2
    assert body["content_sections"][0]["phase_key"] == "observation"
    assert body["content_sections"][0]["media_note"] == "Schéma non numérisé, page 3."
    assert body["content_sections"][1]["media_note"] is None


def test_admin_lesson_detail_with_null_content_sections_does_not_crash(client):
    """Reproduit le cas des Lesson sans contenu structure encore redige (la
    grande majorite des Lesson existantes) : content_sections=None doit etre
    accepte et retourne tel quel, sans erreur."""
    lesson = _seed_lesson(status=ValidationStatus.TO_REVIEW, content_sections=None)
    headers = _admin_headers(client)

    response = client.get(f"/admin/lessons/{lesson.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["content_sections"] is None


def test_admin_lesson_detail_requires_admin(client):
    lesson = _seed_lesson(status=ValidationStatus.TO_REVIEW, content_sections=None)
    assert client.get(f"/admin/lessons/{lesson.id}").status_code == 401


def test_admin_lesson_detail_unknown_id_returns_404(client):
    headers = _admin_headers(client)
    response = client.get(f"/admin/lessons/{uuid.uuid4()}", headers=headers)
    assert response.status_code == 404


def test_public_lesson_detail_404_when_not_published(client):
    lesson = _seed_lesson(status=ValidationStatus.TO_REVIEW, content_sections=SAMPLE_SECTIONS)
    response = client.get(f"/public/lessons/{lesson.id}")
    assert response.status_code == 404


def test_public_lesson_detail_returns_content_sections_when_published(client):
    lesson = _seed_lesson(status=ValidationStatus.PUBLISHED, content_sections=SAMPLE_SECTIONS)
    response = client.get(f"/public/lessons/{lesson.id}")
    assert response.status_code == 200
    body = response.json()
    assert len(body["content_sections"]) == 2
    assert body["content_sections"][0]["title_ar"] == "ألاحظ"


def test_public_lesson_detail_unknown_id_returns_404(client):
    response = client.get(f"/public/lessons/{uuid.uuid4()}")
    assert response.status_code == 404


def test_second_lesson_content_sections_independent_from_first(client):
    """Couvre le cas de la 2e leçon pilote (العين والرّؤية) : deux Lesson
    distinctes, chacune avec ses 8 phases propres, ne doivent jamais se
    melanger ni s'ecraser l'une l'autre."""
    first_lesson = _seed_lesson(
        status=ValidationStatus.TO_REVIEW,
        content_sections=SAMPLE_SECTIONS,
        title_ar="تركيبة العين",
    )
    second_lesson = _seed_lesson(
        status=ValidationStatus.TO_REVIEW,
        content_sections=SAMPLE_SECTIONS_SECOND_LESSON,
        title_ar="العين والرّؤية",
    )
    headers = _admin_headers(client)

    first_response = client.get(f"/admin/lessons/{first_lesson.id}", headers=headers)
    second_response = client.get(f"/admin/lessons/{second_lesson.id}", headers=headers)

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    first_body = first_response.json()
    second_body = second_response.json()

    assert len(first_body["content_sections"]) == 2
    assert len(second_body["content_sections"]) == 8

    second_phase_keys = [s["phase_key"] for s in second_body["content_sections"]]
    assert second_phase_keys == [
        "mobilisation_acquis",
        "observation",
        "hypothese",
        "experimentation",
        "conclusion",
        "application",
        "evaluation",
        "vocabulaire",
    ]
    # Seules les phases 4 et 6 ont un media_note dans ce jeu de donnees.
    with_media = [s["order"] for s in second_body["content_sections"] if s["media_note"]]
    assert with_media == [4, 6]

    # Aucune fuite de contenu entre les deux leçons.
    assert first_body["content_sections"] != second_body["content_sections"]
