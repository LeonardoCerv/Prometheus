"""
FastAPI Server for Prometheus Recruitment Agent
Exposes agent functionality through REST endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import sys
import os

# Add conversation_agent to path to import the agent
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from conversation_agent.my_agent.agent import (
    progressive_search,
    calculate_match_score,
    reset_search,
    generate_job_description
)

# Initialize FastAPI app
app = FastAPI(
    title="Prometheus Recruitment API",
    description="API for intelligent candidate search and matching through conversational filtering",
    version="1.0.0"
)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== REQUEST/RESPONSE MODELS ====================

class SearchRequest(BaseModel):
    query: str = Field(..., description="Natural language search query", example="I need a React developer")
    reset_conversation: bool = Field(False, description="Start a fresh search, clearing previous filters")

class SearchResponse(BaseModel):
    status: str
    conversation_turn: int
    current_query: str
    combined_filters: Dict[str, Any]
    total_candidates_searched: int
    matches_found: int
    matches: List[Dict[str, Any]]
    refinement_suggestion: str

class MatchScoreRequest(BaseModel):
    candidate_name: str = Field(..., description="Name of the candidate", example="Maria Garcia")
    job_title: str = Field(..., description="Job title or position", example="Senior React Developer")

class MatchScoreResponse(BaseModel):
    status: str
    candidate: Optional[str] = None
    job: Optional[str] = None
    score: Optional[float] = None
    reasoning: Optional[str] = None
    strengths: Optional[List[str]] = None
    gaps: Optional[List[str]] = None
    recommendation: Optional[str] = None
    message: Optional[str] = None

class ResetResponse(BaseModel):
    status: str
    message: str

class JobDescriptionResponse(BaseModel):
    status: str
    conversation_turns: Optional[int] = None
    queries: Optional[List[str]] = None
    required_skills: Optional[List[str]] = None
    experience_level: Optional[str] = None
    availability: Optional[str] = None
    candidates_matching: Optional[int] = None
    message: Optional[str] = None

# ==================== HEALTH CHECK ====================

@app.get("/")
def root():
    """Root endpoint - API health check"""
    return {
        "message": "Prometheus Recruitment API is running",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "search": "/api/search",
            "match_score": "/api/match-score",
            "reset": "/api/reset",
            "job_description": "/api/job-description",
            "health": "/api/health"
        }
    }

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Prometheus Recruitment API"}

# ==================== SEARCH ENDPOINT ====================

@app.post("/api/search", response_model=SearchResponse)
def search_candidates(request: SearchRequest):
    """
    Progressive candidate search endpoint.
    
    Each search query refines previous results unless reset_conversation is True.
    
    Examples:
    - First query: "I need a React developer"
    - Follow-up: "only senior level"
    - Follow-up: "with Next.js experience"
    """
    try:
        result = progressive_search(
            query=request.query,
            reset_conversation=request.reset_conversation
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== MATCH SCORE ENDPOINT ====================

@app.post("/api/match-score", response_model=MatchScoreResponse)
def calculate_match(request: MatchScoreRequest):
    """
    Calculate semantic compatibility score between a candidate and job.
    
    Returns a score (0-100) with detailed reasoning, strengths, and gaps.
    """
    try:
        result = calculate_match_score(
            candidate_name=request.candidate_name,
            job_title=request.job_title
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== RESET ENDPOINT ====================

@app.post("/api/reset", response_model=ResetResponse)
def reset_search_state():
    """
    Reset the progressive search to start fresh.
    
    Clears all previous filters and conversation context.
    """
    try:
        result = reset_search()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== JOB DESCRIPTION ENDPOINT ====================

@app.post("/api/job-description", response_model=JobDescriptionResponse)
def create_job_description():
    """
    Generate a job description based on the search conversation.
    
    Analyzes all queries and filters to create a comprehensive job description.
    Requires at least one search query to have been made.
    """
    try:
        result = generate_job_description()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== CONVERSATION STATE ENDPOINT ====================

@app.get("/api/conversation-state")
def get_conversation_state():
    """
    Get the current conversation state and history.
    
    Returns the number of turns, queries made, and candidates remaining.
    """
    try:
        from conversation_agent.my_agent.agent import get_progressive_filter
        progressive_filter = get_progressive_filter()
        summary = progressive_filter.get_conversation_summary()
        return {
            "status": "success",
            **summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 Starting Prometheus Recruitment API Server")
    print("="*60)
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📖 ReDoc Documentation: http://localhost:8000/redoc")
    print("="*60 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
