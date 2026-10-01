#!/usr/bin/env python3
"""Weighted Meta Ads audit score (claude-ads scoring model, MIT). Stdlib only.

  audit_score.py checks.json
  audit_score.py --selftest

checks.json = [{"id":"M01","category":"pixel","severity":"critical","result":"pass",
                "title":"Pixel installed","fix_minutes":5}, ...]
category: pixel | creative | structure | audience     (weights 30/30/20/20)
severity: critical | high | medium | low              (5 / 3 / 1.5 / 0.5)
result:   pass | warning | fail | na                  (1 / 0.5 / 0 / excluded)
"""
import json
import sys

CAT = {"pixel": 0.30, "creative": 0.30, "structure": 0.20, "audience": 0.20}
SEV = {"critical": 5.0, "high": 3.0, "medium": 1.5, "low": 0.5}
RES = {"pass": 1.0, "warning": 0.5, "fail": 0.0}
GRADES = [(90, "A", "Excellent"), (75, "B", "Good"), (60, "C", "Needs improvement"), (40, "D", "Poor"), (0, "F", "Critical")]


def score(checks):
    got = possible = 0.0
    by_cat = {}
    for c in checks:
        r = c["result"].lower()
        if r == "na":
            continue
        w = SEV[c["severity"].lower()] * CAT[c["category"].lower()]
        got += RES[r] * w
        possible += w
        g, p = by_cat.get(c["category"], (0.0, 0.0))
        by_cat[c["category"]] = (g + RES[r] * w, p + w)
    total = round(got / possible * 100, 1) if possible else 0.0
    grade = next((g, label) for floor, g, label in GRADES if total >= floor)
    cats = {k: round(g / p * 100, 1) for k, (g, p) in by_cat.items() if p}
    quick = [c for c in checks if c["result"].lower() == "fail"
             and c["severity"].lower() in ("critical", "high") and c.get("fix_minutes", 99) <= 15]
    return total, grade, cats, quick


def selftest():
    checks = [
        {"id": "M01", "category": "pixel", "severity": "critical", "result": "pass"},
        {"id": "M02", "category": "pixel", "severity": "critical", "result": "fail", "fix_minutes": 15},
        {"id": "M25", "category": "creative", "severity": "critical", "result": "warning"},
        {"id": "M33", "category": "structure", "severity": "medium", "result": "na"},
    ]
    total, grade, cats, quick = score(checks)
    # got = 1.5 + 0 + 0.75 = 2.25 ; possible = 1.5*3 = 4.5 -> 50.0
    assert total == 50.0 and grade[0] == "D", (total, grade)
    assert cats == {"pixel": 50.0, "creative": 50.0}
    assert [q["id"] for q in quick] == ["M02"]
    assert score([{"id": "x", "category": "audience", "severity": "low", "result": "pass"}])[1][0] == "A"
    print("audit_score.py selftest OK")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        return selftest()
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    checks = json.load(open(sys.argv[1], encoding="utf-8"))
    total, (g, label), cats, quick = score(checks)
    print(f"# Meta Ads health: {total}/100 — grade {g} ({label})\n")
    print("| Category | Score |\n|---|---|")
    for k in CAT:
        if k in cats:
            print(f"| {k} | {cats[k]} |")
    fails = sorted((c for c in checks if c["result"].lower() in ("fail", "warning")),
                   key=lambda c: (-SEV[c["severity"].lower()], c["result"].lower() != "fail"))
    if fails:
        print("\n## Issues (most severe first)\n| ID | Severity | Result | Check |\n|---|---|---|---|")
        for c in fails:
            print(f"| {c['id']} | {c['severity']} | {c['result']} | {c.get('title', '')} |")
    if quick:
        print("\n## Quick wins (Critical/High, < 15 min)")
        for c in quick:
            print(f"- {c['id']} {c.get('title', '')} (~{c.get('fix_minutes')} min)")


if __name__ == "__main__":
    main()
