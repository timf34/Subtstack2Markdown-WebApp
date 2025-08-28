# Requirements

## Functional Requirements

### Must Have (P0)
- [ ] POST /api/jobs accepts `{url, email?, password?}` and returns `{jobId}`.
- [ ] GET /api/jobs/{id}/status returns `{state, progressPct, message?, hasDownload}`.
- [ ] GET /api/jobs/{id}/download returns a ZIP archive or `404` if not ready.
- [ ] `/health` endpoint returns basic JSON.
- [ ] Scraper collects public posts and premium posts if login succeeds.
- [ ] Package Markdown and HTML versions plus an index page into a single ZIP stored in `dist/` with 24h retention.
- [ ] Frontend submits jobs, polls status, and enables ZIP download when complete.

### Should Have (P1)
- [ ] Structured JSON logging with `jobId` correlation.
- [ ] Concurrency controls, retries, and robots.txt compliance.
- [ ] Automatic cleanup of expired ZIP files.

### Nice to Have (P2)
- [ ] Metrics for jobs created/succeeded/failed.

## Technical Requirements

### Performance
- Async `httpx` requests with concurrency ≤ 8 and exponential backoff.
- Idempotent Celery tasks; Redis as broker and state store.

### Security
- Do not persist or log credentials.
- Mask secrets in logs/traces.

### Compatibility
- Python 3.11+, Node 18+, Docker-based dev environment.

## Constraints
- Respect Substack terms of service and robots.txt.
- On CAPTCHA or login failure continue with public scraping and surface state accordingly.
- All work lives inside this project unless explicitly allowed below.

## Out of Scope
- Bypassing paywalls or anti-bot measures.
- Long-term storage of scraped content.

## Shared Code Allowed Outside Project
The following top-level paths may be modified by this project:

- `/app` – FastAPI service code.
- `/scraper` – scraping and transformation modules.
- `/docker` – Dockerfiles and compose files.
- `/tests` – backend tests.
- `/web` – Next.js frontend.
- `.env.example` – environment variable template.
- `.gitignore` – additions for new directories.
