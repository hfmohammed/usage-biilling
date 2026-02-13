"""
Pytest fixtures: in-memory DB, test user, and FastAPI client with auth override.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Import app after we set env so test DB is not used by imports
from database import Base, get_db
from models.user import UserDB
from models.account import AccountDB
import models.purchase
import models.user
import models.account
import models.transaction
import models.portfolio
import models.holding
import models.trade


TEST_USER_ID = "test-user-id-12345"
TEST_USER_EMAIL = "test@test.com"


def _ensure_accounts_name_column(engine):
    """Add accounts.name if missing (test DB may have been created without it)."""
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE accounts ADD COLUMN name VARCHAR NOT NULL DEFAULT ''"))
            conn.commit()
        except Exception as e:
            err = str(e).lower()
            if "duplicate column name" not in err and "no such table" not in err:
                raise
            conn.rollback()


@pytest.fixture(scope="function")
def db_engine():
    """In-memory SQLite engine for each test (isolated)."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # single connection so :memory: is shared
    )
    # Create tables in FK order (users first, then accounts)
    UserDB.__table__.create(bind=engine, checkfirst=True)
    AccountDB.__table__.create(bind=engine, checkfirst=True)
    _ensure_accounts_name_column(engine)
    yield engine
    AccountDB.__table__.drop(bind=engine, checkfirst=True)
    UserDB.__table__.drop(bind=engine, checkfirst=True)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Session bound to the test engine."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def test_user(db_session: Session) -> UserDB:
    """Create a test user in the DB (required for account FK)."""
    user = UserDB(
        user_id=TEST_USER_ID,
        name="Test User",
        email=TEST_USER_EMAIL,
        password_hash="hashed",
        phone="",
        address="",
        city="",
        state="",
        zip="",
        country="",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def override_get_db(session: Session):
    def _get_db():
        yield session
    return _get_db


def override_get_current_user(test_user: UserDB):
    def _get_current_user():
        return test_user
    return _get_current_user


@pytest.fixture(scope="function")
def client(db_session: Session, test_user: UserDB):
    """FastAPI TestClient with get_db and get_current_user overridden."""
    from app import app
    from auth.deps import get_current_user

    app.dependency_overrides[get_db] = override_get_db(db_session)
    app.dependency_overrides[get_current_user] = override_get_current_user(test_user)

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client_no_auth(db_engine, db_session):
    """Client with get_db override but no auth (for testing 401)."""
    from app import app

    app.dependency_overrides[get_db] = override_get_db(db_session)
    # do NOT override get_current_user so Bearer is required

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
