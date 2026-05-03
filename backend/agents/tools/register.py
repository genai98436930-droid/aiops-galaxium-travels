from db import SessionLocal
from services import flight, booking, user


# =========================================================
# DB WRAPPER (SINGLE SOURCE OF TRUTH)
# =========================================================
def safe_tool(fn):
    """
    Ensures every tool:
    - gets a fresh DB session
    - never depends on context["db"]
    - always closes DB safely
    """
    def wrapper(context: dict):
        db = SessionLocal()
        try:
            context = dict(context or {})
            return fn(db, context)
        finally:
            db.close()

    return wrapper


# =========================================================
# TOOL IMPLEMENTATIONS (CLEAN CONTRACT)
# =========================================================

def list_flights(db, context):
    return flight.list_flights(db)


def book_flight(db, context):
    return booking.book_flight(
        db,
        context.get("user_id"),
        context.get("name"),
        context.get("flight_id"),
        context.get("seat_class", "economy"),
    )


def get_bookings(db, context):
    return booking.get_bookings(db, context.get("user_id"))


def cancel_booking(db, context):
    return booking.cancel_booking(db, context.get("booking_id"))


def register_user(db, context):
    name = context.get("name")
    email = context.get("email")

    if not name or not email:
        return {
            "success": False,
            "error": "Missing name or email",
            "error_code": "INVALID_INPUT"
        }

    return user.register_user(db, name, email)


import inspect

def get_user(db, context):
    name = context.get("name")
    email = context.get("email")

    fn = user.get_user

    params = inspect.signature(fn).parameters

    # CASE 1: (db, name, email)
    if len(params) == 3:
        return fn(db, name, email)

    # CASE 2: (db, name=email combo or user_id)
    if len(params) == 2:
        return fn(db, context.get("user_id") or email or name)

    # SAFE FALLBACK
    raise ValueError(f"Unsupported get_user signature: {params}")


# =========================================================
# TOOL REGISTRATION
# =========================================================
def register_tools(registry):
    registry.register("list_flights", safe_tool(list_flights))
    registry.register("book_flight", safe_tool(book_flight))
    registry.register("get_bookings", safe_tool(get_bookings))
    registry.register("cancel_booking", safe_tool(cancel_booking))
    registry.register("register_user", safe_tool(register_user))
    registry.register("get_user", safe_tool(get_user))