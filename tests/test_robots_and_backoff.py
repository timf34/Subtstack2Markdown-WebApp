import httpx
import respx
import pytest

from scraper import public_client


@respx.mock
def test_respects_robots(tmp_path):
    respx.get("https://example.com/robots.txt").respond(200, text="User-agent: *\nDisallow: /feed")
    with pytest.raises(PermissionError):
        public_client.fetch_public_posts("https://example.com/feed")


@respx.mock
def test_backoff_retry(monkeypatch):
    call = respx.get("https://example.com/feed").mock(side_effect=[
        httpx.Response(429, headers={"Retry-After": "0"}),
        httpx.Response(200, text="<rss><channel></channel></rss>"),
    ])
    respx.get("https://example.com/robots.txt").respond(200, text="User-agent: *\nAllow: /")
    public_client._robot_cache.clear()
    posts, author = public_client.fetch_public_posts("https://example.com/feed")
    assert author == "substack"
    assert posts == []
    assert call.call_count == 2
