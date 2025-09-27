from fastapi import APIRouter
# Import the 'router' object from our newly named 'endpoints.py' file
from ..users.endpoints import router as users_router

api_router = APIRouter()

# Now we include the router object we just imported and renamed
api_router.include_router(users_router, prefix="/users", tags=["Users"])