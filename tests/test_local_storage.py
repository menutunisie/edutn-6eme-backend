import uuid

import pytest

from app.db.session import SessionLocal
from app.main import app
from app.models.enums import ValidationStatus
from app.models.resource import Resource
from app.models.resource_type import ResourceType
from app.services.local_storage import LocalFileStorageService, build_lesson_media_path
from app.services.storage import get_storage_service
from tests.test_lesson_detail import _seed_lesson

BASE_URL = "http://testserver"
CONTENT = b"\x89PNG-fake-schema-bytes"


@pytest.fixture
def storage(tmp_path):
    service = LocalFileStorageService(root=tmp_path, base_url=BASE_URL)
    app.dependency_overrides[get_storage_service] = lambda: service
    yield service
    app.dependency_overrides.pop(get_storage_service, None)


def _seed_resource(lesson_id, file_ref, status=ValidationStatus.TO_REVIEW):
    db = SessionLocal()
    try:
        resource_type = ResourceType(
            code=f"TYPE_{uuid.uuid4().hex[:8]}", name_fr="Type test", name_ar="نوع"
        )
        db.add(resource_type)
        db.flush()
        db.add(
            Resource(
                lesson_id=lesson_id,
                resource_type_id=resource_type.id,
                status=status,
                file_ref=file_ref,
            )
        )
        db.commit()
    finally:
        db.close()


def test_upload_serve_delete_roundtrip(client, storage, tmp_path):
    lesson = _seed_lesson(status=ValidationStatus.TO_REVIEW, content_sections=None)
    path = build_lesson_media_path(lesson.id, "schema-p10.png")

    assert storage.upload(path, CONTENT, "image/png") == path
    assert (tmp_path / "lesson-media" / str(lesson.id) / "schema-p10.png").read_bytes() == CONTENT
    _seed_resource(lesson.id, path)

    url = storage.get_url(path)
    assert url == f"{BASE_URL}/media/lessons/{lesson.id}/schema-p10.png"

    response = client.get(url.removeprefix(BASE_URL))
    assert response.status_code == 200
    assert response.content == CONTENT
    assert response.headers["content-type"] == "image/png"

    storage.delete(path)
    assert client.get(url.removeprefix(BASE_URL)).status_code == 404
    storage.delete(path)  # idempotent


def test_upload_refuses_existing_file_and_replace_overwrites(storage):
    path = build_lesson_media_path(uuid.uuid4(), "a.png")
    storage.upload(path, b"v1")
    with pytest.raises(FileExistsError):
        storage.upload(path, b"v2")
    storage.replace(path, b"v2")
    assert storage.resolve_path(path).read_bytes() == b"v2"
    with pytest.raises(FileNotFoundError):
        storage.replace(build_lesson_media_path(uuid.uuid4(), "missing.png"), b"x")


def test_media_404_without_resource_or_when_archived(client, storage):
    lesson = _seed_lesson(status=ValidationStatus.TO_REVIEW, content_sections=None)
    path = build_lesson_media_path(lesson.id, "orphan.png")
    storage.upload(path, CONTENT)
    url = f"/media/lessons/{lesson.id}/orphan.png"

    assert client.get(url).status_code == 404  # fichier sur disque, mais aucune Resource

    _seed_resource(lesson.id, path, status=ValidationStatus.ARCHIVED)
    assert client.get(url).status_code == 404  # Resource archivee


def test_storage_rejects_path_traversal(storage):
    lesson_id = uuid.uuid4()
    for bad_path in [
        f"lesson-media/{lesson_id}/../../secret.txt",
        f"lesson-media/{lesson_id}/..%2Fsecret",
        f"other-prefix/{lesson_id}/a.png",
        "lesson-media/not-a-uuid/a.png",
        f"lesson-media/{lesson_id}/.hidden",
    ]:
        with pytest.raises(ValueError):
            storage.upload(bad_path, b"x")


def test_media_route_rejects_invalid_filename(client, storage):
    lesson = _seed_lesson(status=ValidationStatus.TO_REVIEW, content_sections=None)
    for bad_name in [".hidden", "..%2Fsecret", "a%5Cb.png"]:
        assert client.get(f"/media/lessons/{lesson.id}/{bad_name}").status_code == 404


def test_factory_returns_local_service_by_default():
    get_storage_service.cache_clear()
    try:
        assert isinstance(get_storage_service(), LocalFileStorageService)
    finally:
        get_storage_service.cache_clear()
