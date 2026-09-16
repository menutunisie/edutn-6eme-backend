# EduTN 6eme — Backend

API de la plateforme educative pour la sixieme annee de l'enseignement de base (Tunisie).

**Etape actuelle : Etape 2 — fondations techniques.** Aucun modele metier, aucune
authentification et aucune logique de contenu ne sont encore implementes : ce fichier
sera complete au fil des prochaines etapes.

## Stack

- FastAPI + Uvicorn
- PostgreSQL + SQLAlchemy 2.0 + Alembic
- Pydantic v2 / pydantic-settings
- Supabase Storage (abstraction `StorageService`, voir `app/services/storage.py`)
- Deploiement cible : Railway

## Structure

```
app/
  core/        # configuration (variables d'environnement)
  db/          # engine SQLAlchemy, session, Base declarative
  models/      # modeles SQLAlchemy (vide pour l'instant)
  schemas/     # schemas Pydantic (vide pour l'instant)
  repositories/# acces aux donnees (vide pour l'instant)
  services/    # logique applicative (StorageService pour l'instant)
  routers/     # endpoints FastAPI (health check pour l'instant)
  main.py      # point d'entree de l'application
alembic/       # migrations de base de donnees
tests/         # tests (a partir de l'etape 9)
```

## Installation locale

Prerequis : Python 3.12+, PostgreSQL accessible localement (ou via Railway).

```bash
python -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # puis renseigner les valeurs reelles
```

## Lancement local

```bash
uvicorn app.main:app --reload
```

L'API est alors disponible sur http://localhost:8000, la documentation interactive
sur http://localhost:8000/docs, et le health check sur http://localhost:8000/health.

## Migrations (Alembic)

Aucune migration n'existe encore puisqu'aucun modele metier n'a ete cree. A partir de
l'etape 3 :

```bash
# generer une migration a partir des modeles SQLAlchemy
alembic revision --autogenerate -m "description du changement"

# appliquer les migrations
alembic upgrade head
```

## Variables d'environnement

Voir `.env.example` pour la liste complete (base de donnees, CORS, Supabase Storage,
JWT). Aucune valeur reelle n'est commitee dans le repo.

## Deploiement (Railway)

Le repo contient un `Dockerfile` et un `railway.json` (builder Dockerfile, commande de
demarrage `uvicorn app.main:app --host 0.0.0.0 --port $PORT`). Railway fournit
automatiquement la variable `$PORT` ainsi que `DATABASE_URL` si un plugin PostgreSQL
est attache au service.
