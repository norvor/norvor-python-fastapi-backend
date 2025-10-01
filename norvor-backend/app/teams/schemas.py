from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from ..models import Tool

class TeamRoleBase(BaseModel):
    user_id: UUID
    team_id: UUID
    role: str = "Member"

class TeamRoleCreate(TeamRoleBase):
    pass

class TeamRole(TeamRoleBase):
    id: UUID

    class Config:
        from_attributes = True

class DataCupBase(BaseModel):
    data_bowl_id: UUID 
    team_role_id: Optional[UUID] = None


class DataCupCreate(DataCupBase):
    pass

class DataCup(DataCupBase):
    id: UUID

    class Config:
        from_attributes = True

class DataBowlBase(BaseModel):
    team_id: UUID
    data_bucket_id: UUID
    master_owner_team: UUID

class DataBowlCreate(DataBowlBase):
    pass

class DataBowl(DataBowlBase):
    id: UUID

    class Config:
        from_attributes = True

class TeamBase(BaseModel):
    name: str
    department_id: UUID
    immutable: bool = False
    active: bool = True
    tools: List[Tool] = []

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: UUID
    team_leader_id: Optional[UUID] = None
    team_roles: List[TeamRole] = []
    data_cups: List[DataCup] = []

    class Config:
        from_attributes = True

class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: UUID
    organization_id: int
    teams: List[Team] = []

    class Config:
        from_attributes = True

class DataBucketBase(BaseModel):
    department_id: UUID

class DataBucketCreate(DataBucketBase):
    pass

class DataBucket(DataBucketBase):
    id: UUID
    data_bowls: List[DataBowl] = []

    class Config:
        from_attributes = True