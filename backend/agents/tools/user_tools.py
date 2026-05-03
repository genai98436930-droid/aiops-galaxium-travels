from db import SessionLocal
from services import user


def create_user_tool(context):
    db = SessionLocal()
    try:
        return user.register_user(db, context["name"], context["email"])
    finally:
        db.close()


def get_user_tool(context):
    db = SessionLocal()
    try:
        return user.get_user(db, context["name"], context["email"])
    finally:
        db.close()