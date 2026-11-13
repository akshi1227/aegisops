import os
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aegisops.db")
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
    compliance_status = Column(String, default="PENDING")