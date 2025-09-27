from fastapi import APIRouter
from ..users import router as users_router

api_router = APIRouter()

# Include the users router
api_router.include_router(users_router, prefix="/users", tags=["Users"])

# New feature routers will be included here in the future
# For example:
# api_router.include_router(crm_router, prefix="/crm", tags=["CRM"])