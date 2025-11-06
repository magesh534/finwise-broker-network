from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .auth import get_db, ensure_admin
from .routers import auth_router, broker_router, admin_router, admin_auth_router

# ✅ Step 1: Initialize FastAPI app FIRST
app = FastAPI(title="FinWise Broker Network")

# ✅ Step 2: Enable CORS so frontend (port 5500) can call backend (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",  # VSCode Live Server
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "*"  # Allow all origins (for local dev)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Step 3: Create all database tables
Base.metadata.create_all(bind=engine)

# ✅ Step 4: Include all routers
app.include_router(auth_router.router)
app.include_router(broker_router.router)
app.include_router(admin_router.router)
app.include_router(admin_auth_router.router)

# ✅ Step 5: Ensure admin user exists on startup
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    ensure_admin(db)
    print("✅ Admin user ensured at startup.")

# ✅ Step 6: Health check endpoint for Render
@app.get("/")
def root():
    return {"message": "Welcome to FinWise Broker Network API"}
