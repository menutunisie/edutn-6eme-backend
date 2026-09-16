# EduTN 6eme — Backend

API de la plateforme educative pour la sixieme annee de l'enseignement de base (Tunisie).

**Etape actuelle : Etape 3 — authentification et roles.** Modeles pedagogiques
(Subject, Lesson, Resource...) et ecrans autres que login/gestion des comptes ne sont
pas encore implementes.

## Stack

- FastAPI + Uvicorn
- PostgreSQL + SQLAlchemy 2.0 + Alembic
- Pydantic v2 / pydantic-settings
- JWT (python-jose) + hash de mot de passe Argon2 (passlib)
- Supabase Storage (abstraction `StorageService`, voir `app/services/storage.py`)
- Deploiement cible : Railway

## Structure

```
app/
  core/        # config, securite (JWT, hash, RBAC), seed du compte admin
  db/          # engine SQLAlchemy, session, Base declarative
  models/      # User, RefreshToken
  schemas/     # schemas Pydantic (auth, user)
  repositories/# acces aux donnees (User, RefreshToken)
  services/    # StorageService, auth_service, user_service
  routers/     # health, auth (/auth/*), admin_users (/admin/users/*)
  main.py      # point d'entree + lifespan (seed admin au demarrage)
alembic/       # migrations de base de donnees
tests/         # tests pytest (auth, roles, rotation du refresh token)
```

## Installation locale

Prerequis : Python 3.12+, PostgreSQL accessible localement (ou via Railway).

```bash
python -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -r requirements-dev.txt   # inclut requirements.txt + pytest/httpx

cp .env.example .env               # puis renseigner les valeurs reelles
```

## Lancement local

```bash
uvicorn app.main:app --reload
```

L'API est alors disponible sur http://localhost:8000, la documentation interactive
sur http://localhost:8000/docs, et le health check sur http://localhost:8000/health.

Au demarrage, si aucun utilisateur ADMIN n'existe en base, un compte est cree
automatiquement a partir de `ADMIN_DEFAULT_EMAIL` / `ADMIN_DEFAULT_PASSWORD` (voir
`.env.example`). Un message de log l'indique clairement — changez ce mot de passe des
la premiere connexion.

## Migrations (Alembic)

```bash
# appliquer les migrations existantes (cree les tables users / refresh_tokens)
alembic upgrade head

# generer une nouvelle migration apres modification des modeles SQLAlchemy
alembic revision --autogenerate -m "description du changement"
```

## Tester le flux d'authentification en local

```bash
# 1. Appliquer les migrations
alembic upgrade head

# 2. Demarrer l'API (le compte admin par defaut est seede automatiquement)
uvicorn app.main:app --reload

# 3. Se connecter avec le compte admin (ADMIN_DEFAULT_EMAIL / ADMIN_DEFAULT_PASSWORD)
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@edutn6.tn", "password": "<mot-de-passe-defini-dans-.env>"}'

# 4. Avec l'access_token recu, creer un eleve ou un enseignant
curl -X POST http://localhost:8000/admin/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"email": "eleve1@edutn6.tn", "full_name": "Eleve Un", "password": "EleveDemo123!", "role": "STUDENT"}'

# 5. Se connecter avec ce nouveau compte
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "eleve1@edutn6.tn", "password": "EleveDemo123!"}'
```

## Tests

```bash
pytest
```

Les tests utilisent une base SQLite jetable (aucune dependance a PostgreSQL) et
couvrent : login reussi/echoue, acces refuse sans token, acces refuse pour un role
insuffisant, creation d'utilisateur par l'admin, compte desactive, rotation et logout
du refresh token.

## Variables d'environnement

Voir `.env.example` pour la liste complete (base de donnees, CORS, Supabase Storage,
JWT, compte admin par defaut). Aucune valeur reelle n'est commitee dans le repo.

## Deploiement (Railway)

Le repo contient un `Dockerfile` et un `railway.json` (builder Dockerfile, commande de
demarrage `uvicorn app.main:app --host 0.0.0.0 --port $PORT`). Railway fournit
automatiquement la variable `$PORT` ainsi que `DATABASE_URL` si un plugin PostgreSQL
est attache au service. Penser a definir `ADMIN_DEFAULT_EMAIL` / `ADMIN_DEFAULT_PASSWORD`
sur l'environnement de production avant le premier demarrage.
