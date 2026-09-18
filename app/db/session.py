from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, pool_pre_ping=True)

if engine.dialect.name == "sqlite":
    # SQLite uniquement (dev/tests ; la prod utilise PostgreSQL) : le mode
    # journal par defaut serialise trop agressivement les acces concurrents
    # entre processus sur Windows (ex. un `alembic upgrade` lance a cote du
    # serveur en cours d'execution peut provoquer un "disk I/O error" cote
    # pool de connexions deja ouvert). WAL autorise des lecteurs concurrents
    # pendant une ecriture ; busy_timeout fait attendre au lieu d'echouer
    # immediatement en cas de verrou bref.
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragmas(dbapi_connection, connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA busy_timeout=5000")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependance FastAPI fournissant une session DB par requete."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
