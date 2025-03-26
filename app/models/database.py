from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class JobDescriptionDB(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    title = Column(String, nullable=True)
    department = Column(String, nullable=True)
    location = Column(String, nullable=True)
    employment_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    analysis_results = relationship("AnalysisResultDB", back_populates="job_description")

class AnalysisResultDB(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"))
    sections = Column(JSON)  # Store sections as JSON
    bias_analysis = Column(JSON)  # Store bias analysis as JSON
    readability_analysis = Column(JSON)  # Store readability analysis as JSON
    seo_analysis = Column(JSON)  # Store SEO analysis as JSON
    overall_score = Column(Float)
    improvement_suggestions = Column(JSON)  # Store suggestions as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job_description = relationship("JobDescriptionDB", back_populates="analysis_results") 