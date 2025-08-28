# Progress Tracker

## File & Folder Plan
- `app/` – FastAPI application (main.py, routes.py, models.py, settings.py, workers/)
- `scraper/` – public_client.py, premium_client.py, parsing.py, transform.py, writer.py
- `web/` – Next.js frontend for submitting jobs and polling status
- `docker/` – api.Dockerfile, worker.Dockerfile, compose.dev.yml
- `tests/` – test_public_scrape.py, test_job_flow.py, test_packaging.py
- Shared assets: `assets/`, `author_template.html`, `.env.example`, README updates

## Milestones
- [x] **Milestone 1**: Planning Complete (Target: 2025-08-27)
- [ ] **Milestone 2**: Design Approved (Target: 2025-09-03)
- [ ] **Milestone 3**: Implementation Complete (Target: 2025-09-17)
- [ ] **Milestone 4**: Testing Complete (Target: 2025-09-24)
- [ ] **Milestone 5**: Deployed to Production (Target: 2025-10-01)

## Current Sprint Tasks

### In Progress
- [ ] Metrics and advanced error handling.

### Done
- [x] Project setup
- [x] Initial plan and requirements drafted
- [x] Scaffold FastAPI app, routes, and models.
- [x] Add Celery worker and Redis integration.
- [x] Implement public scraper with concurrency and retries.
- [x] Package Markdown/HTML output into ZIP with index.
- [x] Build Next.js frontend for job submission and polling.
- [x] Create Dockerfiles and docker-compose.dev setup.
- [x] Provide `.env.example` and retention cleanup.
- [x] Write backend and packaging tests.
- [x] Update root README with quickstart and ToS note.
- [x] Implement premium scraper with Playwright and CAPTCHA handling.
- [x] Add robots.txt checks and exponential backoff.
- [x] Add mocked premium login and robots tests.
- [x] Extend E2E test for ZIP contents.
- [x] Switch Docker base image to bullseye to fix Playwright dependency install.

## Detailed Task Breakdown

### Planning Phase
- [x] Create project structure
- [x] Gather requirements
- [ ] Write user stories
- [ ] Get stakeholder approval

### Design Phase
- [ ] Create technical design
- [ ] Review with team
- [ ] Update based on feedback

### Implementation Phase
- [x] FastAPI backend and job endpoints
- [x] Celery worker and Redis config
- [x] Public scraper modules
- [x] Premium scraper modules
- [x] Packaging and retention cleanup
- [x] Next.js frontend

### Testing Phase
- [x] Write unit and integration tests
- [x] Run tests
- [x] Fix issues

### Deployment Phase
- [x] Dockerize API and worker
- [ ] Deploy web frontend
- [ ] Monitor
