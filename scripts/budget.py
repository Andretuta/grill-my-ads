#!/usr/bin/env python3
"""Budget math for Meta Ads (stdlib only).

  budget.py min --cpa 40 [--events 50] [--adsets 1]   minimum daily budget to exit learning
  budget.py cents 30.5                                  amount -> MCP cents (3050)
  budget.py gross --amount 100 --tax 0.1215 [--prepaid] tax effect (BR 2026 = 12.15%)
  budget.py ladder --start 50 [--step 0.2] [--steps 6]  vertical scaling plan (+20% every 48-72h)
  budget.py --selftest
"""
import argparse
import sys
from decimal import Decimal, ROUND_HALF_UP


def to_cents(amount):
    return int((Decimal(str(amount)) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def min_daily(cpa, events=50, adsets=1):
    # ponytail: (CPA x 50) / 7 is a practitioner heuristic, not a Meta rule.
    return round(cpa * events / 7 * adsets, 2)


def gross(amount, tax, prepaid):
    """prepaid: tax comes out of the amount added; postpaid: tax is billed on top."""
    if prepaid:
        media = amount / (1 + tax)
        return {"paid": round(amount, 2), "media": round(media, 2), "tax": round(amount - media, 2)}
    return {"paid": round(amount * (1 + tax), 2), "media": round(amount, 2), "tax": round(amount * tax, 2)}


def ladder(start, step=0.2, steps=6):
    out, b = [], start
    for i in range(steps):
        out.append((i, round(b, 2)))
        b *= 1 + step
    return out


def selftest():
    assert to_cents(30) == 3000 and to_cents(30.5) == 3050 and to_cents("5.19") == 519
    assert min_daily(40) == 285.71
    assert min_daily(7, adsets=2) == 100.0
    g = gross(100, 0.1215, prepaid=True)
    assert g["media"] == 89.17 and g["tax"] == 10.83
    assert gross(100, 0.1215, prepaid=False)["paid"] == 112.15
    assert ladder(100, 0.2, 3) == [(0, 100), (1, 120.0), (2, 144.0)]
    print("budget.py selftest OK")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        return selftest()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("min"); m.add_argument("--cpa", type=float, required=True)
    m.add_argument("--events", type=int, default=50); m.add_argument("--adsets", type=int, default=1)
    c = sub.add_parser("cents"); c.add_argument("amount")
    g = sub.add_parser("gross"); g.add_argument("--amount", type=float, required=True)
    g.add_argument("--tax", type=float, default=0.1215); g.add_argument("--prepaid", action="store_true")
    l = sub.add_parser("ladder"); l.add_argument("--start", type=float, required=True)
    l.add_argument("--step", type=float, default=0.2); l.add_argument("--steps", type=int, default=6)
    a = p.parse_args()

    if a.cmd == "min":
        d = min_daily(a.cpa, a.events, a.adsets)
        print(f"Min daily budget: {d:.2f}/day ({to_cents(d)} cents) for {a.events} events/week "
              f"at CPA {a.cpa:.2f} across {a.adsets} ad set(s).")
        print(f"Weekly: {d*7:.2f}. Below this: optimize for a cheaper event or use 1 ad set.")
    elif a.cmd == "cents":
        print(to_cents(a.amount))
    elif a.cmd == "gross":
        g = gross(a.amount, a.tax, a.prepaid)
        print(f"Paid {g['paid']:.2f} | media {g['media']:.2f} | tax {g['tax']:.2f} "
              f"({'prepaid' if a.prepaid else 'postpaid'}, tax {a.tax:.2%})")
    elif a.cmd == "ladder":
        print("| Step | Day (every 48-72h) | Daily budget | Cents |\n|---|---|---|---|")
        for i, b in ladder(a.start, a.step, a.steps):
            print(f"| {i} | ~{i*3} | {b:.2f} | {to_cents(b)} |")
        print("Advance only while CPA holds within target; hold or step back if it rises >20%.")


if __name__ == "__main__":
    main()
