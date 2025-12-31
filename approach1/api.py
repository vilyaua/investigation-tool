#!/usr/bin/env python3
"""
FastAPI REST API for MCP Investigation Tool
Enables integration with Lovable.dev frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from datetime import datetime
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor

from src.crew import MCPInvestigationCrew

# Create FastAPI app
app = FastAPI(
    title="MCP Investigation API",
    description="REST API for multi-agent MCP tool architecture investigations",
    version="1.0.0"
)

# Enable CORS for Lovable frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Lovable domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thread pool for running investigations
executor = ThreadPoolExecutor(max_workers=3)


class InvestigationRequest(BaseModel):
    """Request model for starting an investigation."""
    topic: str
    depth: str = "comprehensive"


class InvestigationResponse(BaseModel):
    """Response model for investigation results."""
    report: str
    topic: str
    depth: str
    started_at: str
    completed_at: str
    duration_seconds: float
    status: str


class InvestigationStatus(BaseModel):
    """Status model for tracking investigation progress."""
    topic: str
    status: str
    phase: str
    message: str


# In-memory storage for investigation status (use Redis in production)
investigation_status = {}


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "MCP Investigation API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/api/investigate", response_model=InvestigationResponse)
async def investigate(request: InvestigationRequest):
    """
    Start a new investigation.

    Args:
        request: Investigation request with topic and depth

    Returns:
        Investigation report and metadata
    """
    if not request.topic or not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic is required")

    if request.depth not in ["quick", "standard", "comprehensive"]:
        raise HTTPException(
            status_code=400,
            detail="Depth must be 'quick', 'standard', or 'comprehensive'"
        )

    try:
        start_time = datetime.now()

        # Update status
        investigation_status[request.topic] = {
            "status": "running",
            "phase": "initializing",
            "message": "Starting investigation..."
        }

        # Run investigation in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        crew = MCPInvestigationCrew(verbose=True)

        def run_investigation():
            return crew.investigate(topic=request.topic, depth=request.depth)

        result = await loop.run_in_executor(executor, run_investigation)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Update status
        investigation_status[request.topic] = {
            "status": "completed",
            "phase": "finished",
            "message": "Investigation complete!"
        }

        return InvestigationResponse(
            report=str(result),
            topic=request.topic,
            depth=request.depth,
            started_at=start_time.isoformat(),
            completed_at=end_time.isoformat(),
            duration_seconds=duration,
            status="completed"
        )

    except Exception as e:
        investigation_status[request.topic] = {
            "status": "failed",
            "phase": "error",
            "message": str(e)
        }
        raise HTTPException(status_code=500, detail=f"Investigation failed: {str(e)}")


@app.get("/api/status/{topic}", response_model=InvestigationStatus)
async def get_status(topic: str):
    """
    Get the status of an investigation.

    Args:
        topic: Investigation topic

    Returns:
        Current investigation status
    """
    if topic not in investigation_status:
        raise HTTPException(status_code=404, detail="Investigation not found")

    status = investigation_status[topic]
    return InvestigationStatus(
        topic=topic,
        status=status["status"],
        phase=status["phase"],
        message=status["message"]
    )


@app.get("/api/recent")
async def list_recent():
    """
    List recent investigations.

    Returns:
        List of recent investigation metadata
    """
    output_dir = Path("outputs")
    if not output_dir.exists():
        return {"investigations": []}

    reports = sorted(
        output_dir.glob("investigation_*.md"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    investigations = []
    for report in reports[:10]:
        timestamp = datetime.fromtimestamp(report.stat().st_mtime)
        topic = report.stem.replace("investigation_", "").replace("_", " ")
        size = report.stat().st_size / 1024  # KB

        investigations.append({
            "topic": topic,
            "filename": report.name,
            "timestamp": timestamp.isoformat(),
            "size_kb": round(size, 1)
        })

    return {"investigations": investigations}


@app.get("/api/report/{filename}")
async def get_report(filename: str):
    """
    Get a specific investigation report.

    Args:
        filename: Report filename

    Returns:
        Report content
    """
    output_dir = Path("outputs")
    report_path = output_dir / filename

    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")

    content = report_path.read_text()
    return {"filename": filename, "content": content}


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
