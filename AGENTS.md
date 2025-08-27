# AGENTS.md — Substack2Markdown Web App (Project Memory)

## Mission
Build a production‑ready web app that:
1) Accepts a Substack publication URL and optional credentials (email+password) from the user.
2) Efficiently scrapes public posts; if credentials are provided and login succeeds, include premium posts.
3) Produces a single downloadable ZIP with Markdown and HTML versions plus an index page.
4) Provides clear job progress and errors (e.g., CAPTCHA detected, login failure).
5) Respects legal and ethical constraints (see “Compliance & Safety”).

## Constraints & Non‑Goals
- Do NOT store raw credentials. Use them in memory for this job only. No logging of secrets. Mask in traces.
- If a CAPTCHA blocks premium login, STOP that premium flow and return a user‑friendly message and partial (public) results.
- Be gentle with rate limits: concurrency <= 8, per‑host delay/backoff, and respect robots.txt.
- DON’T bypass paywalls. Only fetch premium posts after a successful user-authenticated session.
- Keep the codebase small, conventional, and easy to deploy on Fly.io + Vercel.

## Architecture
- Backend: FastAPI (Python 3.11+), Uvicorn.
- Worker: Celery + Redis (Upstash or local). Jobs are idempotent; job state persisted in Redis.
- Premium scraping: Playwright Chromium in a **separate worker** process. Headless; user agent randomized; hardware acceleration disabled for server.
- Public scraping: httpx (async), selectolax or BeautifulSoup, exponential backoff, ETag/Last-Modified handling, and a 10s timeout default.
- Packaging: create `dist/<author>-<YYYYMMDD>.zip` including:
  - `data/<author>.json` (consolidated metadata for UI)
  - `substack_md_files/<author>/*.md`
  - `substack_html_pages/<author>/*.html`
  - `substack_html_pages/<author>.html` (index)
- Frontend: Next.js minimal UI (URL field, optional email/password, submit -> job page -> download).
- Deploy: Docker + docker-compose for dev; Fly.io for API+worker; Vercel or Fly for frontend.

## Directory Layout (target)
.
├── app/                       # FastAPI app
│   ├── main.py                # app factory, routes
│   ├── routes.py              # /api/jobs endpoints
│   ├── models.py              # pydantic schemas
│   ├── security.py            # secret masking, input validation
│   ├── settings.py            # pydantic Settings (reads env)
│   └── workers/
│       ├── celery_app.py
│       ├── tasks.py           # queue jobs, report progress
│       └── playwright_login.py
├── scraper/
│   ├── public_client.py       # httpx async fetcher
│   ├── premium_client.py      # Playwright flows
│   ├── parsing.py             # soup/selectolax parsing
│   ├── transform.py           # html→md, md→html, metadata merge
│   └── writer.py              # write files, dedupe, zips
├── web/                       # Next.js frontend (or simple static page)
│   └── ...
├── assets/                    # keep your css/js
├── substack_scraper.py        # keep for reference; refactor pieces into scraper/
├── author_template.html
├── docker/
│   ├── api.Dockerfile
│   ├── worker.Dockerfile
│   └── compose.dev.yml
├── tests/
│   ├── test_public_scrape.py
│   ├── test_markdown_convert.py
│   └── test_job_flow.py
├── .env.example
├── REQUIREMENTS.md            # functional & non-functional requirements
├── PROGRESS_TRACKER.md        # detailed checklist; keep up to date
└── README.md

## Functional Requirements (concise)
- POST /api/jobs: body { url, email?, password? }
  - Validates URL (must be a Substack publication root).
  - Creates a job; returns { jobId } and initial state.
- GET /api/jobs/{id}/status: returns { state, progressPct, message?, hasDownload }
- GET /api/jobs/{id}/download: returns application/zip or 404 if not ready.
- Public scraping default: all posts (or “N latest” if query param provided). Premium: only if login works.
- Generate both Markdown and HTML per post and an index page using existing `author_template.html` + your CSS.
- Compress output to a single .zip; store in `dist/` with retention policy (e.g., 24h).

## Non-Functional Requirements
- Robust error handling with human-readable error messages:
  - network timeouts
  - 4xx/5xx
  - captcha or login error
- Logging: JSON logs with jobId correlation IDs.
- Observability: /health endpoint; basic metrics (jobs created/succeeded/failed).
- Security: never print credentials; mask into `******`.
- Rate limiting and polite crawling; read robots.txt and back off on 429.

## Premium Login Flow (playwright_login.py)
- Navigate to https://substack.com/sign-in
- Use “sign in with password” path if available; wait for navigation complete.
- Detect errors:
  - Element with id `error-container` or visible captcha → return {premiumEnabled:false, reason}
- On success, persist cookies **in memory only** for this run; close context after.

## Implementation Plan (what to build, in order)
1) Scaffold FastAPI app + Redis + Celery; define /api/jobs and job states.
2) Port existing parsing & transform logic into `scraper/` modules; switch to httpx async.
3) Implement sitemap/feed discovery and concurrency with retry; unit tests for parser/transform.
4) Implement premium login with Playwright; detect login & captcha; fall back to public-only.
5) Integrate writer/packager (zip) + index page generation using your template/CSS.
6) Frontend: simple form → create job → poll status → enable “Download ZIP” button.
7) Hardening: input validation, logging, retention cleanup (cron in worker).
8) CI: run tests on PR; container build.
9) Deploy manifests: docker-compose (dev), Fly.io (api+worker), Vercel (web).

## Definition of Done
- `pnpm test` (frontend) and `pytest` (backend) pass locally and in CI.
- `docker compose -f docker/compose.dev.yml up` brings up Redis, API, worker, and you can complete a sample job end‑to‑end.
- Public scraping for a mid‑size publication completes within minutes with polite concurrency.
- Premium flow returns a clear message if CAPTCHA encountered; otherwise includes premium posts.

## Compliance & Safety
- Credentials are provided by the user and must be handled ephemerally and securely.
