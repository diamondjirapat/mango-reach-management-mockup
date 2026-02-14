from sqlalchemy.orm import Session
from . import models, schemas
import random

def get_ads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AdsData).offset(skip).limit(limit).all()

def create_ad(db: Session, ad: schemas.AdsCreate):
    db_ad = models.AdsData(**ad.dict())
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad

def get_dashboard_stats(db: Session):
    total_projects = db.query(models.AdsData).count()
    total_clicks = db.query(models.AdsData).with_entities(models.AdsData.click_count).all()
    total_cost = db.query(models.AdsData).with_entities(models.AdsData.cost).all()
    all_scores = db.query(models.AdsData).with_entities(models.AdsData.score).all()
    
    total_clicks_sum = sum([c[0] for c in total_clicks])
    total_cost_sum = sum([c[0] for c in total_cost])
    avg_score = sum([s[0] for s in all_scores]) / total_projects if total_projects > 0 else 0
    
    return {
        "total_projects": total_projects,
        "total_clicks": total_clicks_sum,
        "total_cost": total_cost_sum,
        "average_score": avg_score
    }
