from sqlalchemy import Column, Integer, String, Float
from .database import Base

class AdsData(Base):
    __tablename__ = "ads_data"
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    project_id = Column(String, index=True)
    source = Column(String)
    source_url = Column(String, nullable=True)
    type = Column(String, default="online")
    click_count = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    score = Column(Float, default=0.0)
