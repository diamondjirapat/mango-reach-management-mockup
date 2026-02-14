from pydantic import BaseModel
from typing import Optional

class AdsBase(BaseModel):
    project_name: str
    project_id: str
    source: str
    source_url: Optional[str] = None
    click_count: int
    cost: float
    score: float

class AdsCreate(AdsBase):
    pass

class Ads(AdsBase):
    id: int

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_projects: int
    total_clicks: int
    total_cost: float
    average_score: float
