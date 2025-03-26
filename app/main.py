from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
from .services.jd_analyzer import JDAnalyzer
from .services.file_processor import FileProcessor
from .models.jd import JobDescription, AnalysisResult

app = FastAPI(
    title="Job Description Analyser",
    description="API for analyzing and enhancing job descriptions",
    version="1.0.0"
)

# Get allowed origins from environment variable
allowed_origins = os.getenv("ALLOWED_ORIGINS", "https://intassist.vercel.app").split()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
jd_analyzer = JDAnalyzer()
file_processor = FileProcessor()

@app.post("/api/analyze/text", response_model=AnalysisResult)
async def analyze_text(jd: JobDescription):
    """
    Analyze a job description provided as text
    """
    try:
        result = await jd_analyzer.analyze_text(jd.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/file", response_model=AnalysisResult)
async def analyze_file(file: UploadFile = File(...)):
    """
    Analyze a job description from an uploaded file
    """
    try:
        content = await file_processor.process_file(file)
        result = await jd_analyzer.analyze_text(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/enhance", response_model=JobDescription)
async def enhance_jd(jd: JobDescription):
    """
    Enhance a job description with suggestions and improvements
    """
    try:
        enhanced_jd = await jd_analyzer.enhance_jd(jd)
        return enhanced_jd
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint with diagnostic information
    """
    try:
        # Check if required environment variables are set
        env_vars = {
            "DATABASE_URL": bool(os.getenv("DATABASE_URL")),
            "HUGGINGFACE_API_KEY": bool(os.getenv("HUGGINGFACE_API_KEY")),
            "JWT_SECRET": bool(os.getenv("JWT_SECRET")),
            "PORT": os.getenv("PORT", "10000"),
            "HOST": os.getenv("HOST", "0.0.0.0")
        }
        
        return {
            "status": "healthy",
            "environment": {
                "variables": env_vars,
                "all_required_set": all(env_vars.values())
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 