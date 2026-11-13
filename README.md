AegisOps
AegisOps is an advanced, full-stack enterprise operations and compliance validation platform featuring an integrated Retrieval-Augmented Generation (RAG) AI engine. It combines high-performance backend processing, automated compliance auditing, and an intelligent assistant to streamline system monitoring and regulatory governance.

🚀 Key Features
Automated Compliance Validation: Audits operational logs and enterprise data against regulatory frameworks to flag discrepancies and ensure real-time governance.

RAG AI Engine: Integrates OpenAI embeddings, LangChain, and a FAISS vector search database for context-aware technical log retrieval and intelligent assistant queries.

FastAPI Backend: Asynchronous API architecture supporting fast logging, structured database management, and robust query handling.

React Frontend: Modern user interface for real-time operations monitoring, compliance reporting, and interacting with the AI assistant.

Data Engineering Integration: Features structured data pipelines utilizing PySpark and reliable database storage.

Containerization & Testing: Fully containerized with Docker and Docker Compose, supported by Pytest for backend testing reliability.

🛠️ Tech Stack
Backend: Python, FastAPI, Uvicorn, SQLAlchemy, LangChain, FAISS, OpenAI API

Frontend: React, Axios, HTML5, CSS3

Data & Ops: PySpark, Docker, Docker Compose, SQLite / PostgreSQL

Testing: Pytest

⚙️ Getting Started Locally
1. Clone the Repository
Bash
git clone https://github.com/akshi1227/aegisops.git
cd aegisops
2. Set Up the Python Virtual Environment
Bash
python -m venv venv
venv\Scripts\activate     # On Windows
# source venv/bin/activate  # On macOS/Linux
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Environment Variables
Set your OpenAI API key in your terminal session:

DOS
set OPENAI_API_KEY=your_actual_openai_api_key_here
5. Run the Application
Start the FastAPI development server using Uvicorn:

Bash
uvicorn main:app --reload --port 8000
Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser to view the interactive Swagger API documentation.
