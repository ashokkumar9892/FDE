"""Week 1 deliverable: console app.

Reads synthetic customers, validates, calculates days-to-renewal,
groups by risk level, and writes a structured JSON report.

    python backend/risk_report.py
"""
import json
from pathlib import Path

from risk import build_report, load_customers

REQUIRED = {"customer_id", "name", "renewal_date", "usage_pct_last_30d",
            "exec_sponsor_active", "open_support_tickets", "last_qbr_days_ago", "nps"}
OUT = Path(__file__).resolve().parent.parent / "data" / "renewal_report.json"


def validate(customers: list[dict]) -> None:
    for c in customers:
        missing = REQUIRED - c.keys()
        if missing:
            raise ValueError(f"{c.get('customer_id', '?')} missing fields: {sorted(missing)}")


def main() -> None:
    customers = load_customers()
    validate(customers)
    report = build_report(customers)

    OUT.write_text(json.dumps(report, indent=2))
    s = report["summary"]
    print(f"Scored {report['total']} customers")
    print(f"  High risk:   {s['High']}")
    print(f"  Medium risk: {s['Medium']}")
    print(f"  Low risk:    {s['Low']}")
    print(f"Report written -> {OUT}")

    top = sorted(
        (r for lvl in report["by_level"].values() for r in lvl),
        key=lambda r: r["risk_score"], reverse=True,
    )[:5]
    print("\nTop 5 at-risk accounts:")
    for r in top:
        print(f"  [{r['risk_score']:>3}] {r['name']:<22} "
              f"({r['days_to_renewal']}d) — {r['reasons'][0]}")


if __name__ == "__main__":
    main()
