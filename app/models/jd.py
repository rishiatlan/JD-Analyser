from pydantic import BaseModel
from typing import List, Optional, Dict

class JobDescription(BaseModel):
    content: str
    title: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None

class Section(BaseModel):
    title: str
    content: str
    suggestions: Optional[List[str]] = None

class BiasAnalysis(BaseModel):
    biased_terms: List[str]
    suggestions: List[str]
    inclusivity_score: float

class ReadabilityAnalysis(BaseModel):
    score: float
    complexity: str
    suggestions: List[str]

class SEOAnalysis(BaseModel):
    keywords: List[str]
    missing_keywords: List[str]
    suggestions: List[str]

class AnalysisResult(BaseModel):
    sections: List[Section]
    bias_analysis: BiasAnalysis
    readability_analysis: ReadabilityAnalysis
    seo_analysis: SEOAnalysis
    overall_score: float
    improvement_suggestions: List[str]

class EnhancedJD(JobDescription):
    enhanced_content: str
    analysis_result: AnalysisResult
    version: int = 1 