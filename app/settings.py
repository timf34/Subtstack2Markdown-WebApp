import os


class Settings:
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    scrape_concurrency: int = int(os.getenv("SCRAPE_CONCURRENCY", "6"))
    zip_retention_hours: int = int(os.getenv("ZIP_RETENTION_HOURS", "24"))
    playwright_headless: bool = os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() == "true"


settings = Settings()
