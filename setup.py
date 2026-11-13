import os

files = {
    "requirements.txt": """fastapi==0.110.0
uvicorn==0.28.0
sqlalchemy==2.0.28
psycopg2-binary==2.9.9
pydantic==2.6.4
pyspark==3.5.0
langchain==0.1.12
faiss-cpu==1.8.0
openai==1.14.1
pytest==8.1.1
python-multipart==0.0.9
axios""",
    
    "database.py": """import os
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/aegisops")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class OperationalLog(Base):
    __tablename__ = "operational_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, index=True)
    log_level = Column(String, index=True)
    message = Column(String)
    status = Column(String)
    compliance_status = Column(String, default="PENDING")""",

    "ai_engine.py": """import os
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-openai-api-key")

def build_vector_store(text_data: str):
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_text(text_data)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(docs, embeddings)
    vectorstore.save_local("faiss_index")
    return vectorstore

def query_aegis_ai(query: str):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)
    return qa_chain.run(query)""",

    "data_pipeline.py": """from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

def run_compliance_pipeline(file_path: str):
    spark = SparkSession.builder.appName("AegisOpsMedicalCompliance").getOrCreate()
    df = spark.read.json(file_path)
    cleaned_df = df.na.drop(subset=["timestamp", "status"])
    flagged_df = cleaned_df.withColumn(
        "compliance_status",
        when((col("status") == "ERROR") | (col("message").contains("PHI_BREACH")), "VIOLATION").otherwise("COMPLIANT")
    )
    flagged_df.write.mode("overwrite").parquet("output/validated_medical_logs.parquet")
    return flagged_df.count()""",

    "main.py": """import database
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
    return {"response": answer}""",

    "test_main.py": """from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_log():
    response = client.post(
        "/logs/",
        json={
            "timestamp": "2026-11-13T10:00:00",
            "log_level": "INFO",
            "message": "Clinical record verified securely",
            "status": "SUCCESS",
            "compliance_status": "COMPLIANT"
        }
    )
    assert response.status_code == 200
    assert response.json()["compliance_status"] == "COMPLIANT"

def test_read_logs():
    response = client.get("/logs/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)""",

    "Dockerfile": """FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]""",

    "docker-compose.yml": """version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/aegisops
      - OPENAI_API_KEY=your-openai-api-key
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=aegisops
    ports:
      - "5432:5432" """
}

os.makedirs("aegisops-frontend/src", exist_ok=True)

for filename, content in files.items():
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

with open("aegisops-frontend/package.json", "w", encoding="utf-8") as f:
    f.write("""{
  "name": "aegisops-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "axios": "^1.6.8",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}""")

with open("aegisops-frontend/src/App.js", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [logs, setLogs] = useState([]);
  const [query, setQuery] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [form, setForm] = useState({ timestamp: '', log_level: 'INFO', message: '', status: 'SUCCESS', compliance_status: 'COMPLIANT' });

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    try {
      const res = await axios.get('http://localhost:8000/logs/');
      setLogs(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/logs/', form);
      fetchLogs();
      setForm({ timestamp: '', log_level: 'INFO', message: '', status: 'SUCCESS', compliance_status: 'COMPLIANT' });
    } catch (err) {
      console.error(err);
    }
  };

  const handleAiQuery = async () => {
    try {
      const res = await axios.post('http://localhost:8000/query/', { query });
      setAiResponse(res.data.response);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: '30px', fontFamily: 'Arial, sans-serif', maxWidth: '900px', margin: '0 auto' }}>
      <h1>AegisOps – Medical Compliance & Audit Dashboard</h1>
      
      <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '5px' }}>
        <h2>AI Compliance Query (RAG)</h2>
        <input 
          type="text" 
          value={query} 
          onChange={(e) => setQuery(e.target.value)} 
          placeholder="Ask about medical compliance or SOPs..." 
          style={{ width: '70%', padding: '8px', marginRight: '10px' }}
        />
        <button onClick={handleAiQuery} style={{ padding: '8px 15px' }}>Ask AI</button>
        {aiResponse && <p style={{ marginTop: '15px', background: '#f4f4f4', padding: '10px', borderRadius: '4px' }}><strong>Response:</strong> {aiResponse}</p>}
      </div>

      <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '5px' }}>
        <h2>Add Compliance Log</h2>
        <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
          <input type="text" placeholder="Timestamp" value={form.timestamp} onChange={(e) => setForm({...form, timestamp: e.target.value})} style={{ padding: '8px' }} />
          <input type="text" placeholder="Log Level" value={form.log_level} onChange={(e) => setForm({...form, log_level: e.target.value})} style={{ padding: '8px' }} />
          <input type="text" placeholder="Message" value={form.message} onChange={(e) => setForm({...form, message: e.target.value})} style={{ padding: '8px' }} />
          <input type="text" placeholder="Status" value={form.status} onChange={(e) => setForm({...form, status: e.target.value})} style={{ padding: '8px' }} />
          <button type="submit" style={{ gridColumn: 'span 2', padding: '10px', background: '#007bff', color: '#fff', border: 'none', cursor: 'pointer' }}>Submit Log Entry</button>
        </form>
      </div>

      <div>
        <h2>System & Compliance Records</h2>
        <table border="1" cellPadding="10" style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ background: '#f8f9fa' }}>
              <th>ID</th>
              <th>Timestamp</th>
              <th>Level</th>
              <th>Message</th>
              <th>Status</th>
              <th>Compliance</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id}>
                <td>{log.id}</td>
                <td>{log.timestamp}</td>
                <td>{log.log_level}</td>
                <td>{log.message}</td>
                <td>{log.status}</td>
                <td>{log.compliance_status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;""")

with open("aegisops-frontend/src/index.js", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);""")

print("SUCCESS: All AegisOps project files have been generated successfully!")