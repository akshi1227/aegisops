import database
from database import SessionLocal, engine
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from ai_engine import query_aegis_ai
from fastapi.middleware.cors import CORSMiddleware

database.Base.metadata.create_all(bind=engine)
app = FastAPI(title="AegisOps Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LogCreate(BaseModel):
    timestamp: str
    log_level: str
    message: str
    status: str
    compliance_status: str

class QueryRequest(BaseModel):
    query: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/logs/")
def create_log(log: LogCreate, db=Depends(get_db)):
    db_log = database.OperationalLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@app.get("/logs/")
def read_logs(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return db.query(database.OperationalLog).offset(skip).limit(limit).all()

@app.post("/query/")
def query_ai(req: QueryRequest):
    answer = query_aegis_ai(req.query)
    return {"response": answer}