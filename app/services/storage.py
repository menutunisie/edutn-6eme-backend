"""Abstraction de stockage de fichiers.

L'interface StorageService permet de brancher n'importe quel provider
(Supabase Storage aujourd'hui, S3/Azure demain) sans impacter le reste
du code applicatif. Aucune logique metier (resources, uploads valides,
permissions) n'est implementee ici : ce sera fait a partir de l'etape 8
(gestion des fichiers).
"""

from abc import ABC, abstractmethod
from functools import lru_cache
from pathlib import Path

from supabase import Client, create_client

from app.core.config import get_settings

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class StorageService(ABC):
    """Interface commune a tous les providers de stockage de fichiers."""

    @abstractmethod
    def upload(self, path: str, content: bytes, content_type: str | None = None) -> str:
        """Envoie un fichier et retourne son chemin de stockage."""

    @abstractmethod
    def get_url(self, path: str) -> str:
        """Retourne une URL (publique ou signee) permettant d'acceder au fichier."""

    @abstractmethod
    def delete(self, path: str) -> None:
        """Supprime un fichier du stockage."""

    @abstractmethod
    def replace(self, path: str, content: bytes, content_type: str | None = None) -> str:
        """Remplace le contenu d'un fichier existant sans changer sa reference."""


class SupabaseStorageService(StorageService):
    """Implementation StorageService basee sur Supabase Storage (S3-compatible)."""

    def __init__(self, client: Client, bucket: str) -> None:
        self._client = client
        self._bucket = bucket

    def upload(self, path: str, content: bytes, content_type: str | None = None) -> str:
        options = {"content-type": content_type} if content_type else None
        self._client.storage.from_(self._bucket).upload(path, content, options)
        return path

    def get_url(self, path: str) -> str:
        return self._client.storage.from_(self._bucket).get_public_url(path)

    def delete(self, path: str) -> None:
        self._client.storage.from_(self._bucket).remove([path])

    def replace(self, path: str, content: bytes, content_type: str | None = None) -> str:
        options = {"content-type": content_type, "upsert": "true"} if content_type else {"upsert": "true"}
        self._client.storage.from_(self._bucket).update(path, content, options)
        return path


@lru_cache
def get_storage_service() -> StorageService:
    """Point d'entree unique du stockage : le provider est choisi par
    STORAGE_PROVIDER. Aucun autre code ne doit instancier un provider."""
    settings = get_settings()
    if settings.storage_provider == "local":
        from app.services.local_storage import LocalFileStorageService

        root = Path(settings.local_storage_root)
        if not root.is_absolute():
            root = PROJECT_ROOT / root
        return LocalFileStorageService(root=root, base_url=settings.media_base_url)

    client = create_client(settings.supabase_url, settings.supabase_key)
    return SupabaseStorageService(client=client, bucket=settings.supabase_storage_bucket)
