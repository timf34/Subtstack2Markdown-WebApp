import os
import time
import urllib.parse
import urllib.robotparser
from pathlib import Path
from typing import List, Tuple

import httpx

from .parsing import parse_feed, Post

CONCURRENCY = int(os.getenv("SCRAPE_CONCURRENCY", "6"))

_robot_cache: dict[str, urllib.robotparser.RobotFileParser] = {}


def _fetch_with_backoff(url: str) -> str:
    delay = 1
    for _ in range(5):
        resp = httpx.get(url, follow_redirects=True, timeout=10)
        if resp.status_code in {429, 500, 502, 503, 504}:
            retry_after = resp.headers.get("Retry-After")
            wait = int(retry_after) if retry_after else delay
            delay *= 2
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.text
    resp.raise_for_status()  # pragma: no cover


def _is_allowed(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme:
        return True
    base = f"{parsed.scheme}://{parsed.netloc}"
    rp = _robot_cache.get(base)
    if not rp:
        robots_url = base + "/robots.txt"
        resp = httpx.get(robots_url)
        rp = urllib.robotparser.RobotFileParser()
        if resp.status_code == 200:
            rp.parse(resp.text.splitlines())
        else:
            rp.parse("")
        _robot_cache[base] = rp
    return rp.can_fetch("*", url)


def fetch_public_posts(url: str) -> Tuple[List[Post], str]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme in {"", "file"}:
        file_path = Path(parsed.path if parsed.scheme else url)
        if not file_path.is_absolute():
            file_path = Path(__file__).resolve().parents[1] / file_path
        xml_text = file_path.read_text()
        author, posts = parse_feed(xml_text)
        return posts, author
    if not _is_allowed(url):
        raise PermissionError("disallowed by robots.txt")
    text = _fetch_with_backoff(url)
    author, posts = parse_feed(text)
    return posts, author
