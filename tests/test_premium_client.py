import pytest

from scraper import premium_client


class DummyPage:
    async def goto(self, *args, **kwargs):
        pass

    async def fill(self, *args, **kwargs):
        pass

    async def click(self, *args, **kwargs):
        pass

    async def wait_for_load_state(self, *args, **kwargs):
        pass

    async def query_selector(self, selector: str):
        return object() if selector in {"#captcha", "text=CAPTCHA"} else None


class DummyContext:
    async def new_page(self):
        return DummyPage()

    async def close(self):
        pass


class DummyBrowser:
    async def new_context(self):
        return DummyContext()

    async def close(self):
        pass


class DummyPlaywright:
    def __init__(self):
        self.chromium = self

    async def launch(self, headless=True):
        return DummyBrowser()


class DummyAsyncPlaywright:
    async def __aenter__(self):
        return DummyPlaywright()

    async def __aexit__(self, exc_type, exc, tb):
        pass


def test_captcha(monkeypatch):
    monkeypatch.setattr(premium_client, "async_playwright", lambda: DummyAsyncPlaywright())
    posts, success, reason = premium_client.fetch_premium_posts("u", "e", "p")
    assert posts == []
    assert success is False
    assert reason == "captcha"
