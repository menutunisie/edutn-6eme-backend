import os

ADMIN_EMAIL = os.environ["ADMIN_DEFAULT_EMAIL"]
ADMIN_PASSWORD = os.environ["ADMIN_DEFAULT_PASSWORD"]


def _login(client, email, password):
    return client.post("/auth/login", json={"email": email, "password": password})


def _auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_login_success(client):
    response = _login(client, ADMIN_EMAIL, ADMIN_PASSWORD)
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["refresh_token"]
    assert body["expires_in"] == 1440 * 60


def test_login_invalid_password(client):
    response = _login(client, ADMIN_EMAIL, "wrong-password")
    assert response.status_code == 401


def test_login_unknown_email(client):
    response = _login(client, "unknown@edutn6.tn", "whatever123")
    assert response.status_code == 401


def test_me_without_token_is_rejected(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_with_valid_token(client):
    tokens = _login(client, ADMIN_EMAIL, ADMIN_PASSWORD).json()
    response = client.get("/auth/me", headers=_auth_header(tokens["access_token"]))
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == ADMIN_EMAIL
    assert body["role"] == "ADMIN"
    assert "password" not in body
    assert "hashed_password" not in body


def test_admin_can_create_user_and_new_user_can_login(client):
    admin_tokens = _login(client, ADMIN_EMAIL, ADMIN_PASSWORD).json()
    headers = _auth_header(admin_tokens["access_token"])

    create_response = client.post(
        "/admin/users",
        json={
            "email": "eleve1@edutn6.tn",
            "full_name": "Eleve Un",
            "password": "EleveDemo123!",
            "role": "STUDENT",
        },
        headers=headers,
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["role"] == "STUDENT"
    assert "password" not in created

    login_response = _login(client, "eleve1@edutn6.tn", "EleveDemo123!")
    assert login_response.status_code == 200


def test_create_user_with_duplicate_email_is_rejected(client):
    admin_tokens = _login(client, ADMIN_EMAIL, ADMIN_PASSWORD).json()
    headers = _auth_header(admin_tokens["access_token"])

    payload = {
        "email": "duplicate@edutn6.tn",
        "full_name": "Doublon",
        "password": "DemoPass123!",
        "role": "STUDENT",
    }
    first = client.post("/admin/users", json=payload, headers=headers)
    assert first.status_code == 201

    second = client.post("/admin/users", json=payload, headers=headers)
    assert second.status_code == 409


def test_non_admin_cannot_access_admin_endpoints(client):
    admin_tokens = _login(client, ADMIN_EMAIL, ADMIN_PASSWORD).json()
    admin_headers = _auth_header(admin_tokens["access_token"])

    client.post(
        "/admin/users",
        json={
            "email": "prof1@edutn6.tn",
            "full_name": "Prof Un",
            "password": "ProfDemo123!",
            "role": "TEACHER",
        },
        headers=admin_headers,
    )

    teacher_tokens = _login(client, "prof1@edutn6.tn", "ProfDemo123!").json()
    teacher_headers = _auth_header(teacher_tokens["access_token"])

    response = client.get("/admin/users", headers=teacher_headers)
    assert response.status_code == 403


def test_disabled_account_cannot_login(client):
    admin_tokens = _login(client, ADMIN_EMAIL, ADMIN_PASSWORD).json()
    headers = _auth_header(admin_tokens["access_token"])

    created = client.post(
        "/admin/users",
        json={
            "email": "eleve.desactive@edutn6.tn",
            "full_name": "Eleve Desactive",
            "password": "EleveDemo123!",
            "role": "STUDENT",
        },
        headers=headers,
    ).json()

    patch_response = client.patch(
        f"/admin/users/{created['id']}", json={"is_active": False}, headers=headers
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["is_active"] is False

    login_response = _login(client, "eleve.desactive@edutn6.tn", "EleveDemo123!")
    assert login_response.status_code == 403


def test_admin_can_reset_user_password(client):
    admin_tokens = _login(client, ADMIN_EMAIL, ADMIN_PASSWORD).json()
    headers = _auth_header(admin_tokens["access_token"])

    created = client.post(
        "/admin/users",
        json={
            "email": "reset.me@edutn6.tn",
            "full_name": "Reset Me",
            "password": "OriginalPass123!",
            "role": "STUDENT",
        },
        headers=headers,
    ).json()

    reset_response = client.patch(f"/admin/users/{created['id']}/reset-password", headers=headers)
    assert reset_response.status_code == 200
    body = reset_response.json()
    assert list(body.keys()) == ["temporary_password"]

    temporary_password = body["temporary_password"]
    assert len(temporary_password) == 14
    assert any(c.isupper() for c in temporary_password)
    assert any(c.islower() for c in temporary_password)
    assert any(c.isdigit() for c in temporary_password)
    assert any(c in "!@#$%^&*()-_=+" for c in temporary_password)

    # L'ancien mot de passe ne fonctionne plus...
    old_login = _login(client, "reset.me@edutn6.tn", "OriginalPass123!")
    assert old_login.status_code == 401

    # ...seul le mot de passe temporaire fonctionne desormais.
    new_login = _login(client, "reset.me@edutn6.tn", temporary_password)
    assert new_login.status_code == 200


def test_refresh_token_rotation(client):
    tokens = _login(client, ADMIN_EMAIL, ADMIN_PASSWORD).json()
    old_refresh_token = tokens["refresh_token"]

    refresh_response = client.post("/auth/refresh", json={"refresh_token": old_refresh_token})
    assert refresh_response.status_code == 200
    new_tokens = refresh_response.json()
    assert new_tokens["refresh_token"] != old_refresh_token

    # L'ancien refresh token a ete revoque par la rotation : le reutiliser doit echouer.
    reuse_response = client.post("/auth/refresh", json={"refresh_token": old_refresh_token})
    assert reuse_response.status_code == 401

    # Le nouveau refresh token, lui, doit fonctionner.
    second_refresh_response = client.post(
        "/auth/refresh", json={"refresh_token": new_tokens["refresh_token"]}
    )
    assert second_refresh_response.status_code == 200


def test_logout_revokes_refresh_token(client):
    tokens = _login(client, ADMIN_EMAIL, ADMIN_PASSWORD).json()

    logout_response = client.post("/auth/logout", json={"refresh_token": tokens["refresh_token"]})
    assert logout_response.status_code == 204

    refresh_response = client.post("/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert refresh_response.status_code == 401
