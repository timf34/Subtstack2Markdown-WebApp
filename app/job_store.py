from typing import Dict

JOB_STORE: Dict[str, dict] = {}


def init_job(job_id: str) -> None:
    JOB_STORE[job_id] = {
        "state": "queued",
        "progressPct": 0,
        "message": None,
        "hasDownload": False,
    }


def update_job(job_id: str, **kwargs) -> None:
    if job_id in JOB_STORE:
        JOB_STORE[job_id].update(kwargs)


def get_job(job_id: str) -> dict:
    return JOB_STORE.get(job_id, None)
