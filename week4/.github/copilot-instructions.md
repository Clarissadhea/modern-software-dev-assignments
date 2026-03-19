# Project Overview
Minimal full-stack starter application. FastAPI backend with SQLite, and a static frontend.

# Architecture & Directories
- Backend entry point: `backend/app/main.py`
- API Routers: `backend/app/routers/*.py`
- Tests: `backend/tests/`

# Absolute Rules for Copilot
1. **Test-Driven**: When asked to add a new endpoint, write the failing test in `backend/tests/` FIRST.
2. **Quality Assurance**: Remind the user to run `make format`, `make lint`, and `make test` after any code modification.
3. **Evidence-Based**: Do not hallucinate imports. Read the existing models and schemas before writing router code.