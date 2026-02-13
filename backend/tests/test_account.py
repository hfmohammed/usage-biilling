"""
Tests for account API: health, list, create, get, update, delete, and auth.
"""
import pytest
from fastapi.testclient import TestClient


BASE = "/api/v1/account"


def test_account_health(client: TestClient):
    """GET /api/v1/account/health returns 200 and message ok."""
    r = client.get(f"{BASE}/health")
    assert r.status_code == 200
    assert r.json() == {"message": "ok"}


def test_list_accounts_requires_auth(client_no_auth: TestClient):
    """Without Bearer token, list_accounts returns 401."""
    r = client_no_auth.get(f"{BASE}/list_accounts")
    assert r.status_code == 401


def test_list_accounts_empty(client: TestClient):
    """List accounts for user with no accounts returns []."""
    r = client.get(f"{BASE}/list_accounts")
    assert r.status_code == 200
    assert r.json() == []


def test_create_account_success(client: TestClient):
    """POST with valid body returns 201 and account with name, type, status, currency."""
    r = client.post(
        BASE + "/",
        json={"name": "Checking", "type": "checking", "status": "active", "currency": "USD"},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Checking"
    assert data["type"] == "checking"
    assert data["status"] == "active"
    assert data["currency"] == "USD"
    assert "account_id" in data
    assert "user_id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_account_duplicate_name_returns_400(client: TestClient):
    """Creating two accounts with same name for same user returns 400."""
    body = {"name": "Savings", "type": "savings", "status": "active", "currency": "USD"}
    r1 = client.post(BASE + "/", json=body)
    assert r1.status_code == 201
    r2 = client.post(BASE + "/", json=body)
    assert r2.status_code == 400
    assert "already exists" in r2.json().get("detail", "").lower()


def test_list_accounts_returns_created(client: TestClient):
    """After creating an account, list_accounts returns it."""
    client.post(
        BASE + "/",
        json={"name": "Main", "type": "checking", "status": "active", "currency": "USD"},
    )
    r = client.get(f"{BASE}/list_accounts")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["name"] == "Main"


def test_get_account_success(client: TestClient):
    """GET /{account_id} returns the account when it belongs to the user."""
    create = client.post(
        BASE + "/",
        json={"name": "GetTest", "type": "checking", "status": "active", "currency": "USD"},
    )
    assert create.status_code == 201
    account_id = create.json()["account_id"]
    r = client.get(f"{BASE}/{account_id}")
    assert r.status_code == 200
    assert r.json()["account_id"] == account_id
    assert r.json()["name"] == "GetTest"


def test_get_account_not_found_returns_404(client: TestClient):
    """GET /{account_id} with non-existent id returns 404."""
    r = client.get(f"{BASE}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404
    assert "not found" in r.json().get("detail", "").lower()


def test_update_account_success(client: TestClient):
    """PUT /{account_id} updates name/type/status/currency and returns 200."""
    create = client.post(
        BASE + "/",
        json={"name": "Old", "type": "checking", "status": "active", "currency": "USD"},
    )
    account_id = create.json()["account_id"]
    r = client.put(
        f"{BASE}/{account_id}",
        json={"name": "Updated", "type": "savings", "status": "inactive", "currency": "EUR"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Updated"
    assert data["type"] == "savings"
    assert data["status"] == "inactive"
    assert data["currency"] == "EUR"


def test_update_account_partial(client: TestClient):
    """PUT with only some fields updates only those."""
    create = client.post(
        BASE + "/",
        json={"name": "Partial", "type": "checking", "status": "active", "currency": "USD"},
    )
    account_id = create.json()["account_id"]
    r = client.put(f"{BASE}/{account_id}", json={"name": "PartialUpdated"})
    assert r.status_code == 200
    assert r.json()["name"] == "PartialUpdated"
    assert r.json()["type"] == "checking"


def test_update_account_not_found_returns_404(client: TestClient):
    """PUT with non-existent account_id returns 404."""
    r = client.put(
        f"{BASE}/00000000-0000-0000-0000-000000000000",
        json={"name": "X"},
    )
    assert r.status_code == 404


def test_delete_account_success(client: TestClient):
    """DELETE /{account_id} returns 200 and removes the account."""
    create = client.post(
        BASE + "/",
        json={"name": "ToDelete", "type": "checking", "status": "active", "currency": "USD"},
    )
    account_id = create.json()["account_id"]
    r = client.delete(f"{BASE}/{account_id}")
    assert r.status_code == 200
    assert "message" in r.json()
    get_r = client.get(f"{BASE}/{account_id}")
    assert get_r.status_code == 404


def test_delete_account_not_found_returns_404(client: TestClient):
    """DELETE with non-existent account_id returns 404."""
    r = client.delete(f"{BASE}/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404
