from fastapi import APIRouter
from ..users.endpoints import router as users_router
from ..crm.endpoints import router as crm_router
from ..pm.endpoints import router as pm_router
from ..hr.endpoints import router as hr_router
from ..organiser.endpoints import router as organiser_router
from ..docs.endpoints import router as docs_router
from ..auth.endpoints import router as auth_router # Import the auth router
# Add this line to import the Requests router
from ..requests.endpoints import router as requests_router

api_router = APIRouter()

# --- Authentication Router ---
# This handles /login, /signup, etc.
api_router.include_router(auth_router, tags=["Authentication"])

# Include the users router
api_router.include_router(users_router, prefix="/users", tags=["Users"])

# Include the CRM router
api_router.include_router(crm_router, prefix="/crm", tags=["CRM"])

# Include the PM router
api_router.include_router(pm_router, prefix="/pm", tags=["Project Management"])

# Include the HR router
api_router.include_router(hr_router, prefix="/hr", tags=["Human Resources"])

# Include the Organiser router
api_router.include_router(organiser_router, prefix="/organiser", tags=["Organiser"])

# Include the Docs router
api_router.include_router(docs_router, prefix="/docs", tags=["Documents"])

# Add this line to include the new Requests router
api_router.include_router(requests_router, prefix="/requests", tags=["Requests"])