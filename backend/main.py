from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas, database, analysis

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000", # Vue dev port
    "http://localhost:5173", # Vite dev port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/ads", response_model=List[schemas.Ads])
def read_ads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ads = crud.get_ads(db, skip=skip, limit=limit)
    return ads

@app.get("/api/dashboard", response_model=schemas.DashboardStats)
def read_dashboard_stats(db: Session = Depends(get_db)):
    stats = crud.get_dashboard_stats(db)
    return stats

@app.post("/api/ads", response_model=schemas.Ads)
def create_ad(ad: schemas.AdsCreate, db: Session = Depends(get_db)):
    if ad.score == 0:
        ad.score = analysis.calculate_score(ad.click_count, ad.cost, ad.source)
    return crud.create_ad(db=db, ad=ad)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Ads Reach Analyzer API is running"}

