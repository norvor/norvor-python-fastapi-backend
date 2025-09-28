from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .api.api_v1 import api_router

# This command creates the database tables if they don't exist
# based on your models.py
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Norvor CRM Backend",
    description="The backend for the Norvor comprehensive CRM platform.",
    version="1.0.0"
)

# --- CORS Middleware ---
# Defines which frontend domains are allowed to communicate with this API
origins = [
    "http://localhost",
    "http://localhost:3000", # Default for local React dev
    "https://api.norvorx.com", # Your deployed API
    "https://norvorx.com",
    "https://www.norvorx.com",
    "https://app.norvorx.com"# Your future frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include API Routers ---
# This is the main line that connects your modular endpoints to the app
app.include_router(api_router, prefix="/api/v1")


# A simple root endpoint to confirm the API is running
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Norvor Backend!"}