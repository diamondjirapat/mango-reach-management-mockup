# Ads Reach Analyzer

**Step-by-step to run**

1. **Database** (Docker):  
   `docker-compose up -d`

2. **Backend**:  
   `pip install -r backend/requirements.txt`  
   `python -m uvicorn backend.main:app --reload`

3. **Frontend**:  
   `cd frontend`  
   `npm install`  
   `npm run dev`
   
---

# Access

Frontend: [http://localhost:5173](http://localhost:5173)  USER/PASS: postgres

Backend: [http://localhost:8000/docs](http://localhost:8000/docs)

---
