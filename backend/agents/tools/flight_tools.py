from db import SessionLocal
from services import flight


def get_flights_tool(context):
    db = SessionLocal()
    try:
        return flight.list_flights(db)
    finally:
        db.close()