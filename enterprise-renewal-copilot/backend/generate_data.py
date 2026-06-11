"""Generate 50 synthetic customer records. No real/employer data.

Run once to (re)create ../data/customers.json:
    python backend/generate_data.py
"""
import json
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)  # deterministic output

DATA = Path(__file__).resolve().parent.parent / "data"
DATA.mkdir(exist_ok=True)

FIRST = ["Acme", "Globex", "Initech", "Umbrella", "Hooli", "Stark", "Wayne",
         "Wonka", "Soylent", "Cyberdyne", "Tyrell", "Aperture", "Massive",
         "Vandelay", "Pied Piper", "Gekko", "Oscorp", "Nakatomi", "Bluth", "Dunder"]
LAST = ["Industries", "Corp", "Systems", "Group", "Holdings", "Labs",
        "Partners", "Solutions", "Global", "Logistics"]
PLANS = ["Starter", "Growth", "Business", "Enterprise"]
REGIONS = ["NA-East", "NA-West", "EMEA", "APAC", "LATAM"]
OWNERS = ["Priya N.", "Marcus L.", "Sofia R.", "Daniel K.", "Aisha B."]


def make_record(i: int) -> dict:
    name = f"{random.choice(FIRST)} {random.choice(LAST)}"
    plan = random.choice(PLANS)
    seats = random.randint(5, 800)
    arr = seats * {"Starter": 120, "Growth": 240, "Business": 480, "Enterprise": 950}[plan]
    renewal = date.today() + timedelta(days=random.randint(-10, 200))
    return {
        "customer_id": f"CUST-{1000 + i}",
        "name": name,
        "region": random.choice(REGIONS),
        "account_owner": random.choice(OWNERS),
        "plan": plan,
        "seats": seats,
        "arr_usd": arr,
        "renewal_date": renewal.isoformat(),
        # signals that drive risk
        "usage_pct_last_30d": round(random.uniform(5, 100), 1),
        "open_support_tickets": random.randint(0, 12),
        "exec_sponsor_active": random.random() > 0.25,
        "last_qbr_days_ago": random.randint(10, 400),
        "nps": random.randint(-30, 80),
    }


def main() -> None:
    records = [make_record(i) for i in range(50)]
    out = DATA / "customers.json"
    out.write_text(json.dumps(records, indent=2))
    print(f"Wrote {len(records)} synthetic customers -> {out}")


if __name__ == "__main__":
    main()
