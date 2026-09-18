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


def test_lesson_with_seven_sections_and_no_vocabulaire_phase(client):
    """Couvre le cas de la 4e leçon pilote (انتثار الضّوء, 1re leçon de l'axe
    الضّوء) : seulement 7 phases, pas de phase "vocabulaire" -- confirme que
    content_sections est une liste libre, sans nombre de phases impose par
    le schema (contrairement aux 2 premieres leçons pilotes, qui en ont 8)."""
    seven_phase_sections = [
        {
            "order": i,
            "phase_key": phase_key,
            "title_ar": f"عنوان تجريبي {i}",
            "title_fr": None,
            "body_ar": f"نص تجريبي للمرحلة {i}",
            "body_fr": None,
            "media_note": "Schéma non numérisé." if i in (1, 4) else None,
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
            ],
            start=1,
        )
    ]
    lesson = _seed_lesson(
        status=ValidationStatus.TO_REVIEW,
        content_sections=seven_phase_sections,
        title_ar="انتثار الضّوء",
    )
    headers = _admin_headers(client)

    response = client.get(f"/admin/lessons/{lesson.id}", headers=headers)
    assert response.status_code == 200
    body = response.json()

    assert len(body["content_sections"]) == 7
    phase_keys = [s["phase_key"] for s in body["content_sections"]]
    assert "vocabulaire" not in phase_keys
    assert phase_keys == [
        "mobilisation_acquis",
        "observation",
        "hypothese",
        "experimentation",
        "conclusion",
        "application",
        "evaluation",
    ]


def test_fifth_lesson_eight_sections_media_notes_on_experimentation_and_application(client):
    """Couvre le cas de la 5e leçon pilote (انعكاس الضّوء, 2e leçon de l'axe
    الضّوء) : 8 phases (retour de "vocabulaire"), avec media_note seulement
    sur "experimentation" (ordre 4) et "application" (ordre 6)."""
    eight_phase_sections = [
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
    lesson = _seed_lesson(
        status=ValidationStatus.TO_REVIEW,
        content_sections=eight_phase_sections,
        title_ar="انعكاس الضّوء",
    )
    headers = _admin_headers(client)

    response = client.get(f"/admin/lessons/{lesson.id}", headers=headers)
    assert response.status_code == 200
    body = response.json()

    assert len(body["content_sections"]) == 8
    phase_keys = [s["phase_key"] for s in body["content_sections"]]
    assert phase_keys == [
        "mobilisation_acquis",
        "observation",
        "hypothese",
        "experimentation",
        "conclusion",
        "application",
        "evaluation",
        "vocabulaire",
    ]
    with_media = [s["order"] for s in body["content_sections"] if s["media_note"]]
    assert with_media == [4, 6]


def test_sixth_lesson_eight_sections_media_notes_on_mobilisation_experimentation_application(
    client,
):
    """Couvre le cas de la 6e et derniere leçon pilote (انكسار الضّوء, 3e
    leçon de l'axe الضّوء -- clot l'Unite 1 "العين والضوء") : 8 phases,
    avec media_note sur "mobilisation_acquis" (ordre 1), "experimentation"
    (ordre 4) et "application" (ordre 6)."""
    eight_phase_sections = [
        {
            "order": i,
            "phase_key": phase_key,
            "title_ar": f"عنوان تجريبي {i}",
            "title_fr": None,
            "body_ar": f"نص تجريبي للمرحلة {i}",
            "body_fr": None,
            "media_note": "Schéma non numérisé." if i in (1, 4, 6) else None,
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
    lesson = _seed_lesson(
        status=ValidationStatus.TO_REVIEW,
        content_sections=eight_phase_sections,
        title_ar="انكسار الضّوء",
    )
    headers = _admin_headers(client)

    response = client.get(f"/admin/lessons/{lesson.id}", headers=headers)
    assert response.status_code == 200
    body = response.json()

    assert len(body["content_sections"]) == 8
    phase_keys = [s["phase_key"] for s in body["content_sections"]]
    assert phase_keys == [
        "mobilisation_acquis",
        "observation",
        "hypothese",
        "experimentation",
        "conclusion",
        "application",
        "evaluation",
        "vocabulaire",
    ]
    with_media = [s["order"] for s in body["content_sections"] if s["media_note"]]
    assert with_media == [1, 4, 6]


def test_math_lesson_content_sections_include_exercices_non_transcrits(client):
    """Couvre le format "structure-representatif" des leçons de
    mathematiques (1re leçon pilote, Axe 1) : chaque phase peut porter un
    champ optionnel exercices_non_transcrits (resume des exercices non
    transcrits integralement), absent des leçons de sciences."""
    math_sections = [
        {
            "order": 1,
            "phase_key": "mobilisation_acquis",
            "title_ar": "أستحضر",
            "title_fr": None,
            "body_ar": "نص تجريبي",
            "body_fr": None,
            "media_note": "Tableau non numérisé.",
            "exercices_non_transcrits": None,
        },
        {
            "order": 2,
            "phase_key": "evaluation_acquis",
            "title_ar": "أقيّم مكتسباتي",
            "title_fr": None,
            "body_ar": "نص تجريبي آخر",
            "body_fr": None,
            "media_note": None,
            "exercices_non_transcrits": "Exercices 4 à 7 (pages 5-6), résumé de leur contenu.",
        },
    ]
    lesson = _seed_lesson(
        status=ValidationStatus.TO_REVIEW,
        content_sections=math_sections,
        title_ar="أوظّف الجمع و الطّرح في مجموعة الأعداد العشريّة",
    )
    headers = _admin_headers(client)

    response = client.get(f"/admin/lessons/{lesson.id}", headers=headers)
    assert response.status_code == 200
    body = response.json()

    assert len(body["content_sections"]) == 2
    assert body["content_sections"][0]["exercices_non_transcrits"] is None
    assert (
        body["content_sections"][1]["exercices_non_transcrits"]
        == "Exercices 4 à 7 (pages 5-6), résumé de leur contenu."
    )

    # Endpoint public : le champ doit aussi transiter une fois la leçon publiée.
    db = SessionLocal()
    try:
        db_lesson = db.get(Lesson, lesson.id)
        db_lesson.status = ValidationStatus.PUBLISHED
        db.commit()
    finally:
        db.close()

    public_response = client.get(f"/public/lessons/{lesson.id}")
    assert public_response.status_code == 200
    public_body = public_response.json()
    assert (
        public_body["content_sections"][1]["exercices_non_transcrits"]
        == "Exercices 4 à 7 (pages 5-6), résumé de leur contenu."
    )


# title_ar exact des 8 Unit "leçon" de Mathematiques (Axe 1 a 9, hors 6/10/11/12
# -- revision/evaluation/jeux, sans Lesson).
_MATH_LESSON_UNIT_TITLES = [
    "أوظّف الجمع و الطّرح في مجموعة الأعداد العشريّة",
    "أتصرّف في وحدات قيس المساحة",
    "أوظّف الضّرب والقسمة في مجموعة الأعداد العشريّة",
    "أوظّف التّعامد والتّوازي ومنصّف الزّاوية في البناءات الهندسيّة",
    "أوظّف الجمع والطرح والضّرب على الأعداد التي تقيس الزّمن",
    "أبني زوايا أقيسها بالدّرجة (120-90-60-30-15)",
    "أبني مثلثا استنادا إلى أقيسة الأضلاع والزّوايا",
    "أتعرّف شبه المنحرف وأرسمه",
]


def test_eight_math_lesson_units_each_have_exactly_one_lesson(client):
    """Reproduit la convention validee pour les 8 Unit "leçon" de
    Mathematiques (Axe 1, 2, 3, 4, 5, 7, 8, 9 -- les Axe 6/10/11/12 sont de
    la revision/evaluation/jeux, sans Lesson) : chacune a exactement 1
    Lesson, dont title_ar est une copie exacte du title_ar de l'Unit
    parente, et content_sections=None est gere proprement quand pas encore
    redige (cas des 7 nouvelles Lesson, seule l'Axe 1 est deja remplie)."""
    db = SessionLocal()
    try:
        school_level = SchoolLevel(
            code=f"math-units-test-{uuid.uuid4()}", name_fr="Niveau test", name_ar="مستوى"
        )
        db.add(school_level)
        db.flush()

        subject = Subject(
            school_level_id=school_level.id,
            code=f"MATH_TEST_{uuid.uuid4()}",
            name_fr="Mathematiques test",
            name_ar="رياضيات",
            color="#2563EB",
        )
        db.add(subject)
        db.flush()

        term = Term(
            subject_id=subject.id, code="T1", name_fr="Premier trimestre", name_ar="الثلاثي الأول"
        )
        db.add(term)
        db.flush()

        unit_ids = []
        for i, title_ar in enumerate(_MATH_LESSON_UNIT_TITLES, start=1):
            unit = Unit(
                term_id=term.id,
                title_fr=None,
                title_ar=title_ar,
                status=ValidationStatus.PUBLISHED,
                display_order=i,
            )
            db.add(unit)
            db.flush()

            lesson = Lesson(
                unit_id=unit.id,
                title_ar=title_ar,
                status=ValidationStatus.TO_REVIEW,
                content_sections=None,
            )
            db.add(lesson)
            db.flush()

            unit_ids.append(unit.id)

        db.commit()
    finally:
        db.close()

    headers = _admin_headers(client)

    for unit_id, expected_title_ar in zip(unit_ids, _MATH_LESSON_UNIT_TITLES):
        list_response = client.get(
            "/admin/lessons", params={"unit_id": str(unit_id)}, headers=headers
        )
        assert list_response.status_code == 200
        lessons = list_response.json()
        assert len(lessons) == 1
        assert lessons[0]["title_ar"] == expected_title_ar

        detail_response = client.get(f"/admin/lessons/{lessons[0]['id']}", headers=headers)
        assert detail_response.status_code == 200
        assert detail_response.json()["content_sections"] is None
