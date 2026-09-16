from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Classe de base declarative SQLAlchemy.

    Les modeles metier (a partir de l'etape 3) heritent de cette classe
    et doivent etre importes dans alembic/env.py pour etre detectes
    par les migrations autogenerate.
    """
