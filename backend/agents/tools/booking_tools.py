from db import SessionLocal
from services import booking


def create_booking_tool(context):
    db = SessionLocal()
    try:
        return booking.book_flight(
            db,
            context["user_id"],
            context["name"],
            context["flight_id"],
            context.get("seat_class", "economy")
        )
    finally:
        db.close()


def get_bookings_tool(context):
    db = SessionLocal()
    try:
        return booking.get_bookings(db, context["user_id"])
    finally:
        db.close()


def cancel_booking_tool(context):
    db = SessionLocal()
    try:
        return booking.cancel_booking(db, context["booking_id"])
    finally:
        db.close()