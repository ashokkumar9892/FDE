# Enterprise Renewal Intelligence Copilot

Portfolio project for the Forward Deployed Engineer roadmap. Uses **synthetic data only** —
no real or employer information. This starter covers Weeks 1–2; later weeks layer on RAG,
tool calling, evals, security, Docker, AWS, MCP, and an Angular dashboard.

## Business problem
Renewal analysts spend hours reviewing fragmented customer, usage, and contract data to find
at-risk accounts. This copilot reduces that to a guided review of minutes — outcome first,
machinery second.

## Structure
```
enterprise-renewal-copilot/
  backend/
    generate_data.py   # creates data/customers.json (50 synthetic records)
    risk.py            # shared, testable renewal-risk logic (pure functions)
    risk_report.py     # Week 1: console app -> data/renewal_report.json
    main.py            # Week 2: FastAPI service with auto Swagger docs
  data/
    customers.json     # generated synthetic data
  tests/
    test_risk.py       # Week 4 pytest starter
  requirements.txt
  README.md
```

## Quick start (Windows / PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# (data/customers.json ships generated; regenerate any time)
python backend\generate_data.py

# Week 1 — console report
python backend\risk_report.py        # writes data\renewal_report.json

# Week 2 — API
uvicorn backend.main:app --reload    # http://127.0.0.1:8000/docs

# Tests
pytest -q
```

On macOS/Linux use `source .venv/bin/activate` and forward slashes.

## API endpoints (Week 2)
| Method | Path | Purpose |
|--------|------|---------|
| GET  | `/health` | liveness check |
| GET  | `/customers` | list (supports `region`, `limit`, `offset`) |
| GET  | `/customers/{customer_id}` | single customer |
| GET  | `/renewal-risk` | scored report grouped by risk level |
| POST | `/renewal-risk` | score one customer by id |

## Roadmap of what comes next
- **Wk 3–4** SQLAlchemy + Postgres, pagination, more tests, Angular search screen
- **Wk 5–6** `/ai/analyze-renewal` (Bedrock, provider interface), RAG over contracts with citations
- **Wk 7–8** read-only tools + tool calling, 25+ question eval suite
- **Wk 9–10** JWT + RBAC into retrieval, prompt-injection defense, audit logs, threat model
- **Wk 11–12** Docker Compose, deploy to AWS ECS/Fargate
- **Wk 13–16** agent workflow, C# MCP server, reliability patterns, Terraform + GitHub Actions
- **Wk 17–24** discovery doc, architecture, demo video, résumé, interview prep, packaging

## Design notes (interview talking points)
- **Rule-based score first, LLM second.** `risk.py` is transparent and testable; the LLM
  (Week 5) adds a second opinion behind a provider interface, not a black box.
- **Pure functions** mean the same logic powers the console app, the API, and the tests.
- **Synthetic data** keeps the project shareable and safe to publish on GitHub.
