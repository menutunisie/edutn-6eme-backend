import itertools

from app.db.session import SessionLocal
from app.models.enums import ValidationStatus
from app.models.lesson import Lesson
from app.models.school_level import SchoolLevel
from app.models.subject import Subject
from app.models.term import Term
from app.models.unit import Unit

_counter = itertools.count()


def _seed_minimal_content(*, lesson_status: ValidationStatus) -> Lesson:
    """Cree le chemin complet SchoolLevel->Subject->Term->Unit->Lesson pour
    un seul statut de Lesson, afin de tester le filtrage de l'endpoint
    public independamment des donnees de la migration de seed. Chaque appel
    utilise des codes uniques (contraintes UNIQUE sur SchoolLevel/Subject)."""
    n = next(_counter)
    db = SessionLocal()
    try:
        school_level = SchoolLevel(code=f"test-level-{n}", name_fr="Niveau test", name_ar="مستوى")
        db.add(school_level)
        db.flush()

        subject = Subject(
            school_level_id=school_level.id,
            code=f"TEST_SUBJECT_{n}",
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

        lesson = Lesson(unit_id=unit.id, title_fr="Lecon test", status=lesson_status)
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson
    finally:
        db.close()


def test_public_lessons_excludes_to_review_status(client):
    _seed_minimal_content(lesson_status=ValidationStatus.TO_REVIEW)

    response = client.get("/public/lessons")
    assert response.status_code == 200
    assert response.json() == []


def test_public_lessons_excludes_draft_and_archived(client):
    _seed_minimal_content(lesson_status=ValidationStatus.DRAFT)
    _seed_minimal_content(lesson_status=ValidationStatus.ARCHIVED)

    response = client.get("/public/lessons")
    assert response.status_code == 200
    assert response.json() == []


def test_public_lessons_includes_published_only(client):
    to_review_lesson = _seed_minimal_content(lesson_status=ValidationStatus.TO_REVIEW)
    published_lesson = _seed_minimal_content(lesson_status=ValidationStatus.PUBLISHED)

    response = client.get("/public/lessons")
    assert response.status_code == 200
    body = response.json()

    returned_ids = {item["id"] for item in body}
    assert str(published_lesson.id) in returned_ids
    assert str(to_review_lesson.id) not in returned_ids
    assert len(body) == 1


def test_public_lessons_requires_no_authentication(client):
    # Aucun header Authorization : l'endpoint public doit repondre 200, pas 401.
    response = client.get("/public/lessons")
    assert response.status_code == 200
