import re
from sqlalchemy.orm import Session

from models import User
from schemas import UserOut, ErrorResponse


# =========================
# VALIDATION
# =========================
def is_valid_email(email: str) -> bool:
    """Validate email format."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None


def normalize_email(email: str) -> str:
    """Normalize email for deterministic lookup."""
    return email.strip().lower()


# =========================
# USER REGISTRATION
# =========================
def register_user(db: Session, name: str, email: str) -> UserOut | ErrorResponse:
    email = normalize_email(email)

    if not is_valid_email(email):
        return ErrorResponse(
            error="Invalid email format",
            error_code="INVALID_EMAIL",
            details="Use format like example@domain.com"
        )

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return ErrorResponse(
            error="Email already registered",
            error_code="EMAIL_EXISTS",
            details=f"User already exists for email '{email}'"
        )

    new_user = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserOut.model_validate(new_user)


# =========================
# USER LOOKUP (FIXED CORE ISSUE)
# =========================
def get_user(db: Session, email: str) -> UserOut | ErrorResponse:
    """
    V2 CLEAN DESIGN:
    User identity is EMAIL ONLY (no name dependency)
    """

    email = normalize_email(email)

    if not is_valid_email(email):
        return ErrorResponse(
            error="Invalid email format",
            error_code="INVALID_EMAIL",
            details="Use format like example@domain.com"
        )

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return ErrorResponse(
            error="User not found",
            error_code="USER_NOT_FOUND",
            details=f"No user exists for email '{email}'"
        )

    return UserOut.model_validate(user)


# =========================
# OPTIONAL COMPATIBILITY WRAPPER (SAFE FOR OLD ROUTER)
# =========================
def get_user_by_name_email(db: Session, name: str, email: str):
    """
    Legacy compatibility layer (can be removed later).
    """
    email = normalize_email(email)

    user = db.query(User).filter(
        User.name == name,
        User.email == email
    ).first()

    if not user:
        return ErrorResponse(
            error="User not found",
            error_code="USER_NOT_FOUND",
            details=f"No match for name='{name}' and email='{email}'"
        )

    return UserOut.model_validate(user)