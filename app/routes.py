import uuid
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from .models import JobCreate, JobCreated, JobStatus
from .job_store import init_job, get_job
from .workers.tasks import run_scrape_job

router = APIRouter()


@router.post("/api/jobs", response_model=JobCreated)
async def create_job(payload: JobCreate) -> JobCreated:
    job_id = uuid.uuid4().hex
    init_job(job_id)
    run_scrape_job.delay(job_id, payload.url, payload.email, payload.password)
    return JobCreated(jobId=job_id)


@router.get("/api/jobs/{job_id}/status", response_model=JobStatus)
async def job_status(job_id: str) -> JobStatus:
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return JobStatus(**job)


@router.get("/api/jobs/{job_id}/download")
async def job_download(job_id: str):
    job = get_job(job_id)
    if not job or not job.get("hasDownload"):
        raise HTTPException(status_code=404, detail="not ready")
    zip_path = Path(job.get("zip_path", ""))
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="file missing")
    return FileResponse(zip_path, media_type="application/zip", filename=zip_path.name)


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}
