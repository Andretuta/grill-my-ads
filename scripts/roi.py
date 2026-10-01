#!/usr/bin/env python3
"""Real ROI per ad: Meta spend joined with the business's own results. Stdlib only.

  roi.py breakeven --margin 0.4
  roi.py report --meta meta.csv --biz biz.csv [--margin 0.4] [--tax 0.1215] [--target-cpa 20]
  roi.py --selftest

meta.csv: ad_name,spend[,meta_results]
biz.csv:  key,results[,revenue][,retained]      (key matches ad_name, e.g. via utm_content)
Decimal separator "," is accepted (e.g. 1.234,56).
"""
import argparse
import csv
import sys


def num(s):
    s = (s or "").strip().replace("R$", "").replace(" ", "")
    if not s:
        return 0.0
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".")
    return float(s)


def breakeven(margin):
    if not 0 < margin <= 1:
        raise ValueError("margin must be a fraction in (0, 1]")
    return 1 / margin


def verdict(roas, be, cpa, target_cpa):
    if roas is not None and be is not None:
        if roas >= 1.25 * be:
            return "SCALE"
        return "KEEP" if roas >= be else "CUT/FIX"
    if cpa is None:
        return "CUT/FIX (no results)"
    if target_cpa:
        return "KEEP" if cpa <= target_cpa else ("CUT/FIX" if cpa > 1.5 * target_cpa else "WATCH")
    return "n/a (give --margin or --target-cpa)"


def build(meta_rows, biz_rows, margin=None, tax=0.0, target_cpa=None):
    biz = {}
    for r in biz_rows:
        k = r["key"].strip()
        b = biz.setdefault(k, {"results": 0.0, "revenue": 0.0, "retained": 0.0, "has_rev": False})
        b["results"] += num(r.get("results")); b["retained"] += num(r.get("retained"))
        if r.get("revenue") not in (None, ""):
            b["revenue"] += num(r["revenue"]); b["has_rev"] = True
    be = breakeven(margin) if margin else None
    rows, tot = [], {"spend": 0.0, "cost": 0.0, "results": 0.0, "revenue": 0.0, "meta": 0.0}
    for r in meta_rows:
        name = r["ad_name"].strip()
        spend = num(r["spend"]); cost = spend * (1 + tax)
        b = biz.get(name, {"results": 0.0, "revenue": 0.0, "retained": 0.0, "has_rev": False})
        res = b["results"]
        cpa = cost / res if res else None
        roas = (b["revenue"] / cost if cost else 0.0) if b["has_rev"] else None
        profit = b["revenue"] * margin - cost if (b["has_rev"] and margin) else None
        meta_res = num(r.get("meta_results"))
        rows.append({"ad": name, "spend": spend, "cost": cost, "results": res, "cpa": cpa,
                     "retained_cost": cost / b["retained"] if b["retained"] else None,
                     "revenue": b["revenue"] if b["has_rev"] else None, "roas": roas, "profit": profit,
                     "over_report": meta_res / res if (meta_res and res) else None,
                     "verdict": verdict(roas, be, cpa, target_cpa)})
        tot["spend"] += spend; tot["cost"] += cost; tot["results"] += res
        tot["revenue"] += b["revenue"]; tot["meta"] += meta_res
    unmatched = sorted(set(biz) - {r["ad_name"].strip() for r in meta_rows})
    return rows, tot, be, unmatched


def fmt(v, pct=False, x=False):
    if v is None:
        return "—"
    return f"{v:.2f}x" if x else (f"{v:.1%}" if pct else f"{v:,.2f}")


def selftest():
    meta = [{"ad_name": "A", "spend": "100", "meta_results": "12"},
            {"ad_name": "B", "spend": "1.000,00", "meta_results": "5"},
            {"ad_name": "C", "spend": "50"}]
    biz = [{"key": "A", "results": "10", "revenue": "400", "retained": "8"},
           {"key": "B", "results": "4", "revenue": "1500"},
           {"key": "Z", "results": "1", "revenue": "10"}]
    rows, tot, be, un = build(meta, biz, margin=0.5, tax=0.0)
    a, b, c = rows
    assert be == 2.0
    assert a["cpa"] == 10.0 and a["roas"] == 4.0 and a["verdict"] == "SCALE" and a["over_report"] == 1.2
    assert a["retained_cost"] == 12.5
    assert b["spend"] == 1000.0 and b["roas"] == 1.5 and b["verdict"] == "CUT/FIX"
    assert c["cpa"] is None and c["verdict"] == "CUT/FIX (no results)"
    assert un == ["Z"]
    rows, *_ = build(meta[:1], biz, tax=0.1215, target_cpa=20)
    # no margin -> verdict falls back to CPA vs target: 112.15 / 10 = 11.2 <= 20
    assert abs(rows[0]["cost"] - 112.15) < 1e-9 and rows[0]["verdict"] == "KEEP"
    assert num("R$ 1.234,56") == 1234.56 and num("1,234.56") == 1234.56
    print("roi.py selftest OK")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        return selftest()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("breakeven"); b.add_argument("--margin", type=float, required=True)
    r = sub.add_parser("report")
    r.add_argument("--meta", required=True); r.add_argument("--biz", required=True)
    r.add_argument("--margin", type=float); r.add_argument("--tax", type=float, default=0.0)
    r.add_argument("--target-cpa", type=float)
    a = p.parse_args()
    if a.cmd == "breakeven":
        print(f"Breakeven ROAS = 1 / {a.margin:.0%} = {breakeven(a.margin):.2f}x  (scale gate ~{1.25*breakeven(a.margin):.2f}x)")
        return
    read = lambda f: list(csv.DictReader(open(f, encoding="utf-8-sig")))
    rows, tot, be, unmatched = build(read(a.meta), read(a.biz), a.margin, a.tax, a.target_cpa)
    print(f"# ROI report (tax {a.tax:.2%}{', breakeven ROAS ' + fmt(be, x=True) if be else ''})\n")
    print("| Ad | Spend | Real cost | Results | Real CPA | Cost/retained | Revenue | ROAS | Profit | Meta over-report | Verdict |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for x in rows:
        print(f"| {x['ad'].replace('|', chr(92) + '|')} | {fmt(x['spend'])} | {fmt(x['cost'])} | {x['results']:g} | {fmt(x['cpa'])} | "
              f"{fmt(x['retained_cost'])} | {fmt(x['revenue'])} | {fmt(x['roas'], x=True)} | {fmt(x['profit'])} | "
              f"{fmt(x['over_report'], x=True)} | {x['verdict']} |")
    cpa = tot["cost"] / tot["results"] if tot["results"] else None
    roas = tot["revenue"] / tot["cost"] if tot["cost"] and tot["revenue"] else None
    print(f"| **Total** | {fmt(tot['spend'])} | {fmt(tot['cost'])} | {tot['results']:g} | {fmt(cpa)} | | "
          f"{fmt(tot['revenue'] or None)} | {fmt(roas, x=True)} | | | |")
    if unmatched:
        print(f"\nBusiness keys with no matching ad (check join / organic): {', '.join(unmatched)}")


if __name__ == "__main__":
    main()
