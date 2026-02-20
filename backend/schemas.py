from pydantic import BaseModel, Field
from typing import Optional

class AdsBase(BaseModel):
    project_name: str
    project_id: str
    source: str
    source_url: Optional[str] = None
    type: str = "online"
    click_count: int
    cost: float
    score: float = Field(default=0.0, ge=0.0, le=10.0)

class AdsCreate(AdsBase):
    score: float = Field(default=0.0, ge=0.0, le=10.0)

class Ads(AdsBase):
    id: int

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_projects: int
    total_clicks: int
    total_cost: float
    average_score: float
