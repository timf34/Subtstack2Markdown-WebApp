from __future__ import annotations
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List
from zipfile import ZipFile
import os

from .parsing import Post
from . import transform

BASE_MD_DIR = Path("substack_md_files")
BASE_HTML_DIR = Path("substack_html_pages")
DIST_DIR = Path("dist")
DATA_DIR = Path("data")
TEMPLATE_FILE = Path("author_template.html")
ASSETS_DIR = Path("assets")


def slugify(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")


def cleanup_old_zips(retention_hours: int) -> None:
    if not DIST_DIR.exists():
        return
    cutoff = datetime.utcnow() - timedelta(hours=retention_hours)
    for file in DIST_DIR.glob("*.zip"):
        if datetime.utcfromtimestamp(file.stat().st_mtime) < cutoff:
            file.unlink(missing_ok=True)


def package(job_id: str, author: str, posts: List[Post]) -> Path:
    retention = int(os.getenv("ZIP_RETENTION_HOURS", "24"))
    cleanup_old_zips(retention)
    md_dir = BASE_MD_DIR / author
    html_dir = BASE_HTML_DIR / author
    md_dir.mkdir(parents=True, exist_ok=True)
    html_dir.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)
    DIST_DIR.mkdir(exist_ok=True)

    index_entries = []
    for post in posts:
        slug = slugify(post.title)
        md_content = transform.html_to_md(post.content_html)
        html_content = transform.md_to_html(md_content)
        md_path = md_dir / f"{slug}.md"
        html_path = html_dir / f"{slug}.html"
        md_path.write_text(md_content)
        html_path.write_text(html_content)
        index_entries.append(
            {
                "title": post.title,
                "subtitle": post.subtitle,
                "date": post.date,
                "mdPath": str(md_path.relative_to(BASE_MD_DIR.parent)),
                "htmlPath": str(html_path.relative_to(BASE_HTML_DIR.parent)),
            }
        )

    # write author index
    template = TEMPLATE_FILE.read_text()
    template = template.replace("<!-- AUTHOR_NAME -->", author)
    index_path = BASE_HTML_DIR / f"{author}.html"
    data_script = json.dumps(index_entries)
    index_html = template.replace(
        '<script type="application/json" id="essaysData"></script>',
        f'<script type="application/json" id="essaysData">{data_script}</script>'
    )
    index_path.write_text(index_html)

    # write data json
    data_path = DATA_DIR / f"{author}.json"
    data_path.write_text(json.dumps(index_entries, indent=2))

    # create zip
    today = datetime.utcnow().strftime("%Y%m%d")
    zip_path = DIST_DIR / f"{author}-{today}.zip"
    with ZipFile(zip_path, "w") as zf:
        for path in [md_dir, html_dir, index_path, data_path]:
            if path.is_dir():
                for file in path.rglob("*"):
                    try:
                        arcname = file.relative_to(Path("."))
                    except ValueError:
                        arcname = file.name
                    zf.write(file, arcname)
            else:
                try:
                    arcname = path.relative_to(Path("."))
                except ValueError:
                    arcname = path.name
                zf.write(path, arcname)
        # include assets for completeness
        for file in ASSETS_DIR.rglob("*"):
            try:
                arcname = file.relative_to(Path("."))
            except ValueError:
                arcname = file.name
            zf.write(file, arcname)
    return zip_path
