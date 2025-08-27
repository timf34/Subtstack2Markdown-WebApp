from typing import Optional
from pydantic import BaseModel


class JobCreate(BaseModel):
    url: str
    email: Optional[str] = None
    password: Optional[str] = None


class JobCreated(BaseModel):
    jobId: str


class JobStatus(BaseModel):
    state: str
    progressPct: int
    message: Optional[str] = None
    hasDownload: bool = False
