"""Core renewal-risk logic. Pure functions = easy to test and reuse.

This module is shared by the Week-1 console script (risk_report.py)
and the Week-2 FastAPI service (main.py).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "customers.json"


@dataclass
class RiskResult:
    customer_id: str
    name: str
    days_to_renewal: int
    risk_score: int          # 0-100, higher = more at risk
    risk_level: str          # Low | Medium | High
    reasons: list[str]


def days_until(renewal_iso: str, today: date | None = None) -> int:
    today = today or date.today()
    return (date.fromisoformat(renewal_iso) - today).days


def score_customer(c: dict, today: date | None = None) -> RiskResult:
    """Transparent, rule-based score. (Week 5 swaps in an LLM second opinion.)"""
    score = 0
    reasons: list[str] = []

    dtr = days_until(c["renewal_date"], today)
    if dtr < 0:
        score += 35; reasons.append("Renewal date has already passed")
    elif dtr <= 30:
        score += 30; reasons.append(f"Renewal in {dtr} days")
    elif dtr <= 60:
        score += 15; reasons.append(f"Renewal approaching ({dtr} days)")

    if c["usage_pct_last_30d"] < 25:
        score += 25; reasons.append(f"Low usage ({c['usage_pct_last_30d']}%)")
    elif c["usage_pct_last_30d"] < 50:
        score += 10; reasons.append(f"Soft usage ({c['usage_pct_last_30d']}%)")

    if not c["exec_sponsor_active"]:
        score += 15; reasons.append("No active executive sponsor")

    if c["open_support_tickets"] >= 6:
        score += 10; reasons.append(f"{c['open_support_tickets']} open support tickets")

    if c["last_qbr_days_ago"] > 180:
        score += 8; reasons.append("No QBR in 6+ months")

    if c["nps"] < 0:
        score += 12; reasons.append(f"Detractor NPS ({c['nps']})")

    score = min(score, 100)
    level = "High" if score >= 55 else "Medium" if score >= 30 else "Low"
    if not reasons:
        reasons.append("Healthy across all tracked signals")

    return RiskResult(
        customer_id=c["customer_id"],
        name=c["name"],
        days_to_renewal=dtr,
        risk_score=score,
        risk_level=level,
        reasons=reasons,
    )


def load_customers(path: Path | None = None) -> list[dict]:
    path = path or DATA_FILE
    return json.loads(path.read_text())


def build_report(customers: list[dict], today: date | None = None) -> dict:
    results = [score_customer(c, today) for c in customers]
    by_level = {"High": [], "Medium": [], "Low": []}
    for r in results:
        by_level[r.risk_level].append(asdict(r))
    summary = {lvl: len(v) for lvl, v in by_level.items()}
    return {"summary": summary, "total": len(results), "by_level": by_level}
