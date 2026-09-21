"""Implementation StorageService sur disque local (developpement).

Meme convention de chemins que celle prevue pour Supabase :
`lesson-media/{lesson_id}/{filename}`. Les fichiers sont servis en lecture
par le backend lui-meme (voir app/routers/media.py).
"""

import re
import uuid
from pathlib import Path

from app.services.storage import StorageService

LESSON_MEDIA_PREFIX = "lesson-media"

# Liste blanche stricte : pas de separateur de chemin, pas de nom commencant
# par un point -- ferme la porte a tout path traversal par construction.
_FILENAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,254}$")


def is_valid_filename(filename: str) -> bool:
    return _FILENAME_RE.fullmatch(filename) is not None


def build_lesson_media_path(lesson_id: uuid.UUID, filename: str) -> str:
    """Chemin de stockage canonique (celui a enregistrer dans Resource.file_ref)."""
    if not is_valid_filename(filename):
        raise ValueError(f"Nom de fichier invalide : {filename!r}")
    return f"{LESSON_MEDIA_PREFIX}/{lesson_id}/{filename}"


class LocalFileStorageService(StorageService):
    def __init__(self, root: Path, base_url: str) -> None:
        self._root = root.resolve()
        self._base_url = base_url.rstrip("/")

    def resolve_path(self, path: str) -> Path:
        """Chemin disque d'un chemin de stockage, apres validation stricte de
        la convention `lesson-media/{uuid}/{filename}`."""
        parts = path.split("/")
        if len(parts) != 3 or parts[0] != LESSON_MEDIA_PREFIX:
            raise ValueError(f"Chemin de stockage invalide : {path!r}")
        lesson_id = uuid.UUID(parts[1])
        canonical = build_lesson_media_path(lesson_id, parts[2])
        target = (self._root / canonical).resolve()
        if not target.is_relative_to(self._root):
            raise ValueError(f"Chemin de stockage hors du dossier racine : {path!r}")
        return target

    def upload(self, path: str, content: bytes, content_type: str | None = None) -> str:
        target = self.resolve_path(path)
        if target.exists():
            raise FileExistsError(f"Le fichier existe deja : {path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return path

    def get_url(self, path: str) -> str:
        target = self.resolve_path(path)
        lesson_id, filename = target.parent.name, target.name
        return f"{self._base_url}/media/lessons/{lesson_id}/{filename}"

    def delete(self, path: str) -> None:
        self.resolve_path(path).unlink(missing_ok=True)

    def replace(self, path: str, content: bytes, content_type: str | None = None) -> str:
        target = self.resolve_path(path)
        if not target.exists():
            raise FileNotFoundError(f"Le fichier n'existe pas : {path}")
        target.write_bytes(content)
        return path
