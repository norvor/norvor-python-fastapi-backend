from fastapi import APIRouter
from ..users.endpoints import router as users_router
from ..crm.endpoints import router as crm_router
from ..pm.endpoints import router as pm_router
from ..hr.endpoints import router as hr_router
from ..docs.endpoints import router as docs_router
from ..auth.endpoints import router as auth_router
from ..requests.endpoints import router as requests_router
from ..organizations.endpoints import router as organizations_router
from ..teams.endpoints import router as teams_router

api_router = APIRouter()

# --- Authentication Router ---
api_router.include_router(auth_router, tags=["Authentication"])

# --- Organization Router ---
api_router.include_router(organizations_router, prefix="/organizations", tags=["Organizations"])
api_router.include_router(teams_router, prefix="/teams", tags=["Teams"])


# --- Main Application Routers ---
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(crm_router, prefix="/crm", tags=["CRM"])
api_router.include_router(pm_router, prefix="/pm", tags=["Project Management"])
api_router.include_router(hr_router, prefix="/hr", tags=["Human Resources"])
api_router.include_router(docs_router, prefix="/docs", tags=["Documents"])
api_router.include_router(requests_router, prefix="/requests", tags=["Requests"])