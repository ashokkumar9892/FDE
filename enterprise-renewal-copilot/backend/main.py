"""Week 2 deliverable: FastAPI service.

Run:
    uvicorn backend.main:app --reload
Then open http://127.0.0.1:8000/docs for auto-generated Swagger/OpenAPI.
"""
from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from risk import load_customers, score_customer, build_report

app = FastAPI(
    title="Enterprise Renewal Copilot",
    description="Synthetic-data renewal-risk API (FDE roadmap portfolio project).",
    version="0.1.0",
)

# CORS so an Angular dev server (Week 4) can call this locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _customers() -> list[dict]:
    return load_customers()


class RiskRequest(BaseModel):
    customer_id: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/customers")
def list_customers(region: str | None = None, limit: int = 50, offset: int = 0) -> dict:
    rows = _customers()
    if region:
        rows = [c for c in rows if c["region"].lower() == region.lower()]
    total = len(rows)
    rows = rows[offset:offset + limit]
    return {"total": total, "count": len(rows), "items": rows}


@app.get("/customers/{customer_id}")
def get_customer(customer_id: str) -> dict:
    for c in _customers():
        if c["customer_id"] == customer_id:
            return c
    raise HTTPException(status_code=404, detail=f"{customer_id} not found")


@app.get("/renewal-risk")
def all_risk() -> dict:
    return build_report(_customers())


@app.post("/renewal-risk")
def renewal_risk(req: RiskRequest) -> dict:
    for c in _customers():
        if c["customer_id"] == req.customer_id:
            return asdict(score_customer(c))
    raise HTTPException(status_code=404, detail=f"{req.customer_id} not found")
