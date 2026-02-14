import random
import requests
import time
from backend import models, database, analysis
from sqlalchemy.orm import Session

def generate_mock_data(n=50):
    db = database.SessionLocal()
    
    sources = ["Facebook", "X", "Instagram", "Google", "TikTok", "Flyers", "Billboard", "Unknown"]
    
    print(f"Generating {n} mock entries...")
    for i in range(n):
        project_id = f"PROJ-{random.randint(1000, 9999)}"
        project_name = f"Project {random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Omega'])} {random.randint(1, 100)}"
        source = random.choice(sources)
        source_url = f"http://{source.lower()}.com/{project_id}"
        click_count = random.randint(10, 10000)
        cost = round(random.uniform(10.0, 5000.0), 2)
        score = analysis.calculate_score(click_count, cost, source)
        
        db_ad = models.AdsData(
            project_name=project_name,
            project_id=project_id,
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
