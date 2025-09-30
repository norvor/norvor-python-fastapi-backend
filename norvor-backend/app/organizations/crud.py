from sqlalchemy.orm import Session
from .. import models
from . import schemas

def get_organization(db: Session, org_id: int):
    """
    Get a single organization by its ID.
    """
    return db.query(models.Organization).filter(models.Organization.id == org_id).first()

def complete_onboarding(db: Session, org_id: int):
    """
    Mark an organization's onboarding as complete.
    """
    db_org = get_organization(db, org_id=org_id)
    if db_org:
        db_org.has_completed_onboarding = True
        db.commit()
        db.refresh(db_org)
    return db_org

# --- ADD THIS NEW FUNCTION ---
def get_sidebar_config(db: Session, org_id: int) -> schemas.SidebarConfig:
    """
    Build the dynamic sidebar configuration from the organiser elements.
    """
    elements = db.query(models.OrganiserElement).filter(
        models.OrganiserElement.organization_id == org_id
    ).all()

    teams = []
    departments = []

    # First pass: identify all teams and departments
    for el in elements:
        if el.type == models.OrganiserElementType.TEAM:
            teams.append(schemas.SidebarItem(id=el.id, name=el.label, modules=[]))
        elif el.type == models.OrganiserElementType.DEPARTMENT:
            departments.append(schemas.SidebarItem(id=el.id, name=el.label, modules=[]))

    # Second pass: associate Norvor Tools with their parent team/department
    for el in elements:
        if el.type == models.OrganiserElementType.NORVOR_TOOL and el.parent_id:
            # Find the parent in teams list
            for team in teams:
                if team.id == el.parent_id:
                    team.modules.append(schemas.SidebarModule(id=el.properties.get('tool_id'), name=el.label))
                    break
            # Find the parent in departments list
            for dept in departments:
                if dept.id == el.parent_id:
                    dept.modules.append(schemas.SidebarModule(id=el.properties.get('tool_id'), name=el.label))
                    break
    
    # Assemble the final config
    sidebar_config = schemas.SidebarConfig(
        groups=[
            schemas.SidebarGroup(title="Teams", items=teams),
            schemas.SidebarGroup(title="Departments", items=departments)
        ]
    )

    return sidebar_config
# ------------------------------------