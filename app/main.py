from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
import logging
from .services.jd_analyzer import JDAnalyzer
from .services.file_processor import FileProcessor
from .models.jd import JobDescription, AnalysisResult
import requests
import time
from datetime import datetime, timedelta
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rate limiting configuration
RATE_LIMIT_REQUESTS = 100  # requests per minute
RATE_LIMIT_WINDOW = 60  # seconds
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Rate limiting storage
request_counts = defaultdict(list)

def check_rate_limit(request: Request):
    client_ip = request.client.host
    current_time = datetime.now()
    
    # Clean old requests
    request_counts[client_ip] = [
        req_time for req_time in request_counts[client_ip]
        if current_time - req_time < timedelta(seconds=RATE_LIMIT_WINDOW)
    ]
    
    # Check rate limit
    if len(request_counts[client_ip]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )
    
    request_counts[client_ip].append(current_time)

def check_file_size(file: UploadFile):
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE/1024/1024}MB"
        )

app = FastAPI(
    title="Job Description Analyser",
    description="API for analyzing and enhancing job descriptions",
    version="1.0.0"
)

# Get allowed origins from environment variable
allowed_origins = os.getenv("ALLOWED_ORIGINS", "https://intassist.vercel.app").split()

# Configure CORS with more specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Only allow necessary methods
    allow_headers=["Content-Type", "Authorization"],  # Only allow necessary headers
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Initialize services
jd_analyzer = JDAnalyzer()
file_processor = FileProcessor()

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error handler caught: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": str(exc)}
    )

@app.post("/api/analyze/text", response_model=AnalysisResult)
async def analyze_text(jd: JobDescription, request: Request):
    """
    Analyze a job description provided as text
    """
    try:
        check_rate_limit(request)
        logger.info(f"Analyzing text for job: {jd.title or 'Untitled'}")
        result = await jd_analyzer.analyze_text(jd.content)
        return result
    except Exception as e:
        logger.error(f"Error analyzing text: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/file", response_model=AnalysisResult)
async def analyze_file(request: Request, file: UploadFile = File(...)):
    """
    Analyze a job description from an uploaded file
    """
    try:
        check_rate_limit(request)
        check_file_size(file)
        logger.info(f"Processing file: {file.filename}")
        content = await file_processor.process_file(file)
        result = await jd_analyzer.analyze_text(content)
        return result
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/enhance", response_model=JobDescription)
async def enhance_jd(jd: JobDescription, request: Request):
    """
    Enhance a job description with suggestions and improvements
    """
    try:
        check_rate_limit(request)
        logger.info(f"Enhancing job description: {jd.title or 'Untitled'}")
        enhanced_jd = await jd_analyzer.enhance_jd(jd)
        return enhanced_jd
    except Exception as e:
        logger.error(f"Error enhancing JD: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check(request: Request):
    """
    Health check endpoint with diagnostic information
    """
    try:
        check_rate_limit(request)
        # Check if required environment variables are set
        env_vars = {
            "DATABASE_URL": bool(os.getenv("DATABASE_URL")),
            "HUGGINGFACE_API_KEY": bool(os.getenv("HUGGINGFACE_API_KEY")),
            "JWT_SECRET": bool(os.getenv("JWT_SECRET")),
            "PORT": os.getenv("PORT", "8000"),
            "HOST": os.getenv("HOST", "0.0.0.0")
        }
        
        # Check if Hugging Face API is accessible
        huggingface_status = "unknown"
        if env_vars["HUGGINGFACE_API_KEY"]:
            try:
                response = requests.get(
                    "https://api-inference.huggingface.co/status",
                    headers={"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"},
                    timeout=5  # Add timeout
                )
                huggingface_status = "healthy" if response.status_code == 200 else "unhealthy"
            except requests.Timeout:
                huggingface_status = "timeout"
            except Exception as e:
                huggingface_status = f"error: {str(e)}"
        
        return {
            "status": "healthy",
            "environment": {
                "variables": env_vars,
                "all_required_set": all(env_vars.values())
            },
            "services": {
                "huggingface_api": huggingface_status
            },
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 