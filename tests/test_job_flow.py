from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app
from app.workers.tasks import celery_app
from scraper import writer


def test_job_flow(tmp_path, monkeypatch):
    monkeypatch.setattr(writer, "BASE_MD_DIR", tmp_path / "md")
    monkeypatch.setattr(writer, "BASE_HTML_DIR", tmp_path / "html")
    monkeypatch.setattr(writer, "DIST_DIR", tmp_path / "dist")
    monkeypatch.setattr(writer, "DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(writer, "ASSETS_DIR", Path("assets"))
    monkeypatch.setattr(writer, "TEMPLATE_FILE", Path("author_template.html"))

    celery_app.conf.task_always_eager = True

    client = TestClient(app)
    resp = client.post("/api/jobs", json={"url": "tests/data/sample_feed.xml"})
    assert resp.status_code == 200
    job_id = resp.json()["jobId"]

    status = client.get(f"/api/jobs/{job_id}/status").json()
    assert status["state"] in {"running", "finished"}

    status = client.get(f"/api/jobs/{job_id}/status").json()
    assert status["hasDownload"] is True

    resp = client.get(f"/api/jobs/{job_id}/download")
    assert resp.status_code == 200
    from zipfile import ZipFile
    from io import BytesIO

    with ZipFile(BytesIO(resp.content)) as zf:
        names = zf.namelist()
        assert any(name.endswith('.md') for name in names)
        assert any(name.endswith('.html') for name in names)
