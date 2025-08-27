import json
from celery.utils.log import get_task_logger
from .celery_app import celery_app
from ..job_store import update_job, get_job
from scraper import public_client, premium_client, writer

logger = get_task_logger(__name__)


@celery_app.task
def run_scrape_job(job_id: str, url: str, email: str | None, password: str | None) -> None:
    update_job(job_id, state="running", progressPct=10)
    try:
        posts, author = public_client.fetch_public_posts(url)
        if email and password:
            premium_posts, success, reason = premium_client.fetch_premium_posts(url, email, password)
            if success:
                posts.extend(premium_posts)
            else:
                update_job(job_id, state=reason or "login_failed", message=reason)
        update_job(job_id, progressPct=60)
        zip_path = writer.package(job_id, author, posts)
        current_state = get_job(job_id).get("state", "finished")
        if current_state == "running":
            current_state = "finished"
        update_job(job_id, state=current_state, progressPct=100, hasDownload=True, zip_path=str(zip_path))
        logger.info(json.dumps({"jobId": job_id, "event": "completed"}))
    except PermissionError as exc:
        logger.error(json.dumps({"jobId": job_id, "event": "robots", "msg": str(exc)}))
        update_job(job_id, state="failed", progressPct=100, message=str(exc))
    except Exception as exc:  # pragma: no cover
        logger.error(json.dumps({"jobId": job_id, "event": "error", "msg": str(exc)}))
        update_job(job_id, state="failed", progressPct=100, message=str(exc))
