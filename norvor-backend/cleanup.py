# Run this Python script or add it temporarily to your main.py
from app.database import engine, Base
from app import models

# Drop all tables and recreate them
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)