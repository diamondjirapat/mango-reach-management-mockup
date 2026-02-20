import random
import requests
import time
from backend import models, database, analysis
from sqlalchemy.orm import Session

def generate_mock_data(n=50):
    db = database.SessionLocal()
    
    sources = ["Facebook", "X", "Instagram", "Google", "TikTok", "Flyers", "Billboard"]
    
    print(f"Generating {n} mock entries...")
    for i in range(n):
        project_id = f"PROJ-{i}"
        project_name = f"Project {random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Omega'])} {random.randint(1, 100)}"
        source = random.choice(sources)
        type = "online" if source not in ["Flyers", "Billboard"] else "offline"
        source_url = f"http://{source.lower()}.com/{project_id}"
        click_count = random.randint(10, 10000)
        cost = round(random.uniform(10.0, 5000.0), 2)
        raw_score = analysis.calculate_score(click_count, cost, source)
        score = round(max(0.0, min(10.0, raw_score)), 2)
        
        db_ad = models.AdsData(
            project_name=project_name,
            project_id=project_id,
            type=type,
            source=source,
            source_url=source_url,
            click_count=click_count,
            cost=cost,
            score=score
        )
        db.add(db_ad)
    
    db.commit()
    db.close()
    print("Data generation complete.")

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=database.engine)
    generate_mock_data()
