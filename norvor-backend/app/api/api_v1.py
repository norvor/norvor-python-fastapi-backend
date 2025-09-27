from fastapi import APIRouter
from ..users.endpoints import router as users_router
from ..crm.endpoints import router as crm_router
from ..pm.endpoints import router as pm_router
# Add this line to import the HR router
from ..hr.endpoints import router as hr_router

api_router = APIRouter()

# Include the users router
api_router.include_router(users_router, prefix="/users", tags=["Users"])

# Include the CRM router
api_router.include_router(crm_router, prefix="/crm", tags=["CRM"])

# Include the PM router
api_router.include_router(pm_router, prefix="/pm", tags=["Project Management"])

# Add this line to include the new HR router
api_router.include_router(hr_router, prefix="/hr", tags=["Human Resources"])