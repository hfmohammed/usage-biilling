"""
Secure password hashing using bcrypt. Never store or log plain passwords.
Uses the bcrypt package directly to avoid passlib/bcrypt version conflicts.
"""
import bcrypt

# Bcrypt has a 72-byte limit on password length
MAX_PASSWORD_BYTES = 72


def _truncate_to_bytes(s: str, max_bytes: int = MAX_PASSWORD_BYTES) -> str:
    """Truncate string to at most max_bytes when UTF-8 encoded."""
    encoded = s.encode("utf-8")
    if len(encoded) <= max_bytes:
        return s
    return encoded[:max_bytes].decode("utf-8", errors="ignore") or s[:1]


def hash_password(plain: str) -> str:
    """Hash a plain-text password. Safe for passwords longer than 72 bytes (truncated)."""
    plain = _truncate_to_bytes(plain)
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(plain.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain password against a stored hash."""
    plain = _truncate_to_bytes(plain)
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
