from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from ..models import Tool

# ===================================================================
# User Schemas (for context within Teams)
# ===================================================================
class UserBase(BaseModel):
    id: UUID
    name: str
    email: str

    class Config:
        from_attributes = True

# ===================================================================
# DataCup Schemas
# ===================================================================
class DataCupBase(BaseModel):
    data_bowl_id: UUID
    team_role_id: Optional[UUID] = None

class DataCupCreate(DataCupBase):
    pass

class DataCupUpdate(BaseModel):
    team_role_id: Optional[UUID] = None

class DataCup(DataCupBase):
    id: UUID
    class Config:
        from_attributes = True

# ===================================================================
# TeamRole Schemas
# ===================================================================
class TeamRoleBase(BaseModel):
    user_id: UUID
    team_id: UUID
    role: str = Field("Member", description="The role of the user within the team, e.g., 'Lead', 'Member', 'Contributor'")

class TeamRoleCreate(TeamRoleBase):
    pass

class TeamRoleUpdate(BaseModel):
    role: Optional[str] = None

class TeamRole(TeamRoleBase):
    id: UUID
    user: UserBase
    data_cup: Optional[DataCup] = None
    class Config:
        from_attributes = True

# ===================================================================
# DataBowl Schemas
# ===================================================================
class DataBowlBase(BaseModel):
    team_id: UUID
    data_bucket_id: UUID
    # --- THIS IS THE FIX ---
    # Made this field optional to match potential database state
    master_owner_team: Optional[UUID] = None
    # -----------------------

class DataBowlCreate(DataBowlBase):
    pass

class DataBowlUpdate(BaseModel):
    master_owner_team: Optional[UUID] = None

class DataBowl(DataBowlBase):
    id: UUID
    data_cups: List[DataCup] = []
    class Config:
        from_attributes = True

# ===================================================================
# Team Schemas
# ===================================================================
class TeamBase(BaseModel):
    name: str
    department_id: UUID
    immutable: bool = Field(False, description="Whether this team can be deleted or not")
    active: bool = Field(True, description="Whether this team is currently active")
    tools: List[Tool] = Field([], description="List of software tools/modules enabled for this team")

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    tools: Optional[List[Tool]] = None
    active: Optional[bool] = None
    team_leader_id: Optional[UUID] = None
    department_id: Optional[UUID] = None

class Team(TeamBase):
    id: UUID
    team_leader_id: Optional[UUID] = None
    team_roles: List[TeamRole] = []
    data_bowl: Optional[DataBowl] = None
    class Config:
        from_attributes = True

# ===================================================================
# DataBucket Schemas
# ===================================================================
class DataBucketBase(BaseModel):
    department_id: UUID

class DataBucketCreate(DataBucketBase):
    pass

class DataBucket(DataBucketBase):
    id: UUID
    data_bowls: List[DataBowl] = []
    class Config:
        from_attributes = True

# ===================================================================
# Department Schemas
# ===================================================================
class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="The name of the department")

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="The new name of the department")

class Department(DepartmentBase):
    id: UUID
    organization_id: int
    teams: List[Team] = []
    data_bucket: Optional[DataBucket] = None
    class Config:
        from_attributes = True