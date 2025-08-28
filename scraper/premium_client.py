import asyncio
from typing import List, Tuple

from playwright.async_api import async_playwright

from .parsing import Post


async def _login_and_fetch(url: str, email: str, password: str) -> Tuple[List[Post], bool, str | None]:
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://substack.com/sign-in", wait_until="networkidle")
        await page.fill("input[type=email]", email)
        await page.fill("input[type=password]", password)
        await page.click("button[type=submit]")
        await page.wait_for_load_state("networkidle")
        if await page.query_selector("#captcha") or await page.query_selector("text=CAPTCHA"):
            await context.close()
            await browser.close()
            return [], False, "captcha"
        await context.close()
        await browser.close()
        # premium scraping not implemented; return empty list
        return [], True, None


def fetch_premium_posts(url: str, email: str, password: str) -> Tuple[List[Post], bool, str | None]:
    return asyncio.run(_login_and_fetch(url, email, password))
