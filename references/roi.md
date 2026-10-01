# `/grill-my-ads roi` — real cost per result & ROI

Meta-reported conversions ≠ business reality. This flow joins **Meta spend** with the **business's own results** (orders, leads that became customers, members who joined and stayed, etc.).

## Steps
1. Ask (grill round): which business data source? (CSV/XLSX export, Google Sheet export, DB query result) · what counts as a result (sale, qualified lead, retained member) · how results map to ads (UTM `utm_content`/`utm_campaign`, coupon code, ad name, date only) · margin % · date range · tax rate (BRL default 12.15%, see [regional-brazil.md](regional-brazil.md)).
2. Pull spend: `ads_get_ad_entities level=ad time_range={...}` fields: name, id, spend, impressions, clicks, results, cost per result (validate with `ads_get_field_context`). Save as `meta.csv` (columns `ad_name,spend,meta_results`).
3. Business file: at least `key,results` (+ optional `revenue`, `retained`). `key` must match the chosen join (ad name or utm_content).
4. Run: `python <skill-dir>/scripts/roi.py report --meta meta.csv --biz biz.csv --margin 0.4 --tax 0.1215`.
5. Report `ads/reports/YYYY-MM-DD-roi.md`: table per ad + totals + verdict + recommendations (each change needs approval). If the join is by date only, say attribution is approximate.

## Formulas
| Metric | Formula |
|---|---|
| Real cost | spend × (1 + tax) |
| Real CPA | real cost / business results |
| ROAS | revenue / real cost |
| **Breakeven ROAS** | 1 / contribution margin % (50% margin → 2.0×) |
| Profit | revenue × margin − real cost |
| MER (blended) | total revenue / total marketing spend |
| LTV:CAC | LTV / real CPA (healthy ≥ 3) |
| Payback | real CPA / (monthly margin per customer) |
| Retention cost | real cost / retained results (e.g. members still in after 30 days) |
| Meta over-report | meta_results / business results |

## Verdicts (per ad) [PR]
| Condition | Verdict |
|---|---|
| ROAS ≥ 1.25 × breakeven | SCALE (+15–20%) |
| breakeven ≤ ROAS < 1.25 × breakeven | KEEP / optimize |
| ROAS < breakeven | CUT or fix (hook/offer/landing) |
| No revenue column, CPA ≤ target | KEEP; CPA > 1.5 × target → CUT |

Post-Jan-2026 attribution changes: compare periods with the same windows only ([tracking.md](tracking.md)).
