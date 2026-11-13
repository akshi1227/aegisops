AegisOps
AegisOps is an advanced, full-stack enterprise operations and retrieval-augmented generation (RAG) platform built with a high-performance FastAPI backend, a responsive React frontend, and an integrated FAISS vector search engine.

Features
FastAPI Backend: Asynchronous API architecture supporting fast logging, query handling, and system monitoring.

RAG AI Engine: Combines OpenAI embeddings, LangChain, and FAISS vector search for context-aware technical log retrieval and intelligent assistant queries.

React Frontend: Modern user interface for real-time querying, monitoring logs, and interacting with the system.

Data Engineering Integration: Features supporting robust data pipelines, SQLite/PostgreSQL support, and PySpark components.

Automated Testing: Integrated with Pytest and Playwright for backend and end-to-end testing reliability.

Tech Stack
Backend: Python 3.10+, FastAPI, Uvicorn, SQLAlchemy, LangChain, FAISS, OpenAI API

Frontend: React, Axios, HTML5, CSS3

Data & Ops: PySpark, Docker, PostgreSQL / SQLite

Testing: Pytest, Playwright

Getting Started Locally
1. Clone the Repository
git clone https://github.com/akshi1227/aegisops.git
cd aegisops

2. Set Up the Python Virtual Environment
python -m venv venv
venv\Scripts\activate     # On Windows

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables
Set your OpenAI API key in your terminal session:
set OPENAI_API_KEY=your_actual_openai_api_key_here

5. Run the Application
Start the FastAPI development server using Uvicorn:
uvicorn main:app --reload --port 8000

Navigate to http://127.0.0.1:8000/docs to view the interactive Swagger API documentation.
