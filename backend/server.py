from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP
from sqlalchemy.orm import Session
from typing import Union, Optional
from dotenv import load_dotenv

import os
import httpx

from db import SessionLocal, init_db, get_db
from seed import seed
from services import flight, user, booking
from schemas import (
    FlightOut,
    BookingOut,
    UserOut,
    ErrorResponse,
    BookingRequest,
    UserRegistration,
)

# ==================== ENV ====================
load_dotenv()

# ==================== MCP SERVER ====================
mcp = FastMCP("Galaxium Booking System")


# ==================== TOOL RUNTIME LAYER ====================
from agents.tools.registry import ToolRegistry
from agents.tools.register import register_tools
from agents.runtime.tool_runtime import ToolRuntime
from agents.runtime.agent_router import AgentRouter
from orchestration.engine import OrchestrationEngine

# Create registry
tool_registry = ToolRegistry()

# Register tools (wraps service layer safely)
register_tools(tool_registry)

# Runtime executor
tool_runtime = ToolRuntime(tool_registry)

# LLM router (pluggable: OpenAI / Ollama later)
router = AgentRouter(
    llm_client=None,
    tool_registry=tool_registry
)

# Orchestration engine
engine = OrchestrationEngine(router, tool_runtime)


# ==================== MCP TOOLS ====================
@mcp.tool()
def list_flights() -> list[FlightOut]:
    db = SessionLocal()
    try:
        return flight.list_flights(db)
    finally:
        db.close()


@mcp.tool()
def book_flight(user_id: int, name: str, flight_id: int, seat_class: str = "economy") -> BookingOut:
    db = SessionLocal()
    try:
        return booking.book_flight(db, user_id, name, flight_id, seat_class)
    finally:
        db.close()


@mcp.tool()
def get_bookings(user_id: int) -> list[BookingOut]:
    db = SessionLocal()
    try:
        return booking.get_bookings(db, user_id)
    finally:
        db.close()


@mcp.tool()
def cancel_booking(booking_id: int) -> BookingOut:
    db = SessionLocal()
    try:
        return booking.cancel_booking(db, booking_id)
    finally:
        db.close()


@mcp.tool()
def register_user(name: str, email: str) -> UserOut:
    db = SessionLocal()
    try:
        return user.register_user(db, name, email)
    finally:
        db.close()


@mcp.tool()
def get_user_id(name: str, email: str) -> UserOut:
    db = SessionLocal()
    try:
        return user.get_user(db, name, email)
    finally:
        db.close()


# MCP app mount
mcp_app = mcp.http_app()


# ==================== LIFESPAN ====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    should_seed = os.getenv("SEED_DEMO_DATA", "true").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

    if should_seed:
        seed()

    yield


# ==================== FASTAPI APP ====================
app = FastAPI(
    title="Galaxium Booking System",
    description="API + Agent Runtime + MCP",
    version="1.0.0",
    lifespan=lifespan,
    root_path="/api",
)


# ==================== AGENT ENDPOINT ====================
@app.post("/agent")
def agent_endpoint(payload: dict):
    return engine.run(payload["input"], payload)


# ==================== CORS ====================
allowed_origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== HEALTH ====================
@app.get("/")
def health():
    return {"status": "OK"}


# ==================== FLIGHTS ====================
@app.get("/flights", response_model=list[FlightOut])
def get_flights(
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    departure_date_from: Optional[str] = None,
    departure_date_to: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    has_economy: Optional[bool] = None,
    has_business: Optional[bool] = None,
    has_galaxium: Optional[bool] = None,
    sort: Optional[str] = None,
    order: Optional[str] = "asc",
    db: Session = Depends(get_db),
):
    return flight.list_flights(
        db=db,
        origin=origin,
        destination=destination,
        departure_date_from=departure_date_from,
        departure_date_to=departure_date_to,
        min_price=min_price,
        max_price=max_price,
        has_economy=has_economy,
        has_business=has_business,
        has_galaxium=has_galaxium,
        sort=sort,
        order=order,
    )


# ==================== BOOKINGS ====================
@app.post("/book", response_model=Union[BookingOut, ErrorResponse])
def book_flight_endpoint(request: BookingRequest, db: Session = Depends(get_db)):
    return booking.book_flight(
        db,
        request.user_id,
        request.name,
        request.flight_id,
        request.seat_class,
    )


@app.get("/bookings/{user_id}", response_model=list[BookingOut])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    return booking.get_bookings(db, user_id)


@app.post("/cancel/{booking_id}", response_model=Union[BookingOut, ErrorResponse])
def cancel_booking_endpoint(booking_id: int, db: Session = Depends(get_db)):
    return booking.cancel_booking(db, booking_id)


# ==================== USERS ====================
@app.post("/register", response_model=Union[UserOut, ErrorResponse])
def register_user_endpoint(request: UserRegistration, db: Session = Depends(get_db)):
    return user.register_user(db, request.name, request.email)


@app.get("/user", response_model=Union[UserOut, ErrorResponse])
def get_user_endpoint(name: str, email: str, db: Session = Depends(get_db)):
    return user.get_user(db, name, email)


# ==================== JAVA SERVICE PROXY ====================
JAVA_SERVICE_URL = os.getenv("JAVA_SERVICE_URL", "http://localhost:8080")


@app.post("/quotes")
async def create_quote(data: dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{JAVA_SERVICE_URL}/api/v1/quotes", json=data)
        return r.json()


@app.get("/quotes/{quote_id}")
async def get_quote(quote_id: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{JAVA_SERVICE_URL}/api/v1/quotes/{quote_id}")
        return r.json()


# ==================== MCP MOUNT ====================
app.mount("/mcp", mcp_app)


# ==================== MAIN ====================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
