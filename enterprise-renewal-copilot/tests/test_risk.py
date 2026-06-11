"""Week 4 starter: pytest. Run from the project root:

    pytest -q
"""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from risk import score_customer, days_until, build_report  # noqa: E402

BASE = {
    "customer_id": "CUST-TEST",
    "name": "Test Co",
    "region": "NA-East",
    "account_owner": "QA",
    "plan": "Growth",
    "seats": 100,
    "arr_usd": 24000,
    "renewal_date": "2026-12-31",
    "usage_pct_last_30d": 90.0,
    "open_support_tickets": 0,
    "exec_sponsor_active": True,
    "last_qbr_days_ago": 30,
    "nps": 60,
}
TODAY = date(2026, 6, 11)


def test_days_until():
    assert days_until("2026-06-21", TODAY) == 10
    assert days_until("2026-06-01", TODAY) == -10


def test_healthy_customer_is_low_risk():
    r = score_customer(BASE, TODAY)
    assert r.risk_level == "Low"
    assert r.risk_score < 30


def test_at_risk_customer_is_high():
    bad = {**BASE, "renewal_date": "2026-06-20", "usage_pct_last_30d": 10.0,
           "exec_sponsor_active": False, "open_support_tickets": 8, "nps": -10}
    r = score_customer(bad, TODAY)
    assert r.risk_level == "High"
    assert "Low usage (10.0%)" in r.reasons


def test_report_groups_all_customers():
    rows = [BASE, {**BASE, "customer_id": "CUST-2", "usage_pct_last_30d": 5.0,
                   "renewal_date": "2026-06-15", "exec_sponsor_active": False}]
    report = build_report(rows, TODAY)
    assert report["total"] == 2
    assert sum(report["summary"].values()) == 2
