# `/grill-my-ads audit` — read-only account audit

Checklist & scoring adapted from claude-ads (MIT, © 2026 agricidaniel / tododeia.com). **Read-only**: no `create/update/activate/delete`. Every proposed change goes in a list that runs only with per-item approval.

## Steps
1. Context: `ads_get_ad_accounts` → pick account (ask if >1). `ads_insights_advertiser_context`.
2. Pull data (validate fields with `ads_get_field_context` first; run any `next_actions` queue):
   - `ads_get_ad_entities level=campaign|adset|ad date_preset=last_28d` with spend, impressions, reach, frequency, CTR, CPC, CPM, results, cost per result, `effective_status`, learning status, `advantage_state_info`.
   - `ads_get_datasets` → `ads_get_dataset_quality`, `ads_get_dataset_stats`.
   - `ads_insights_performance_trend`, `ads_insights_anomaly_signal`, `ads_insights_industry_benchmark`, `ads_insights_auction_ranking_benchmarks`.
   - `ads_get_errors`, `ads_account_get_activity_logs` (recent edits → learning resets), `ads_get_opportunity_score`.
   - Creatives: `ads_get_creatives` (formats, count per ad set, age).
3. Evaluate each check → PASS / WARNING / FAIL / NA. Unknown data → NA and say why.
4. Write `checks.json` and run `python <skill-dir>/scripts/audit_score.py checks.json` → score, grade, quick wins.
5. Report `ads/reports/YYYY-MM-DD-audit.md`: score + grade, table by category, top 5 fixes (impact × effort), proposed changes (each needs approval).
No campaigns? Say so, skip to the setup checks (pixel, CAPI, domain, Page/IG, payment) and recommend `/grill-my-ads`.

## Checks (id · severity · pass rule)
### Pixel / CAPI (weight 30%)
| ID | Sev | Pass |
|---|---|---|
| M01 | Critical | Pixel firing on all key pages |
| M02 | Critical | CAPI active (not legacy Offline Conversions API) |
| M03 | Critical | Dedup via `event_id` ≥ 90% |
| M04 | Critical | EMQ: Purchase ≥ 8.5 (warn 6–8.4), others ≥ 6 |
| M05 | High | Domain verified |
| M07 | High | Standard events used |
| M10 | Medium | Events fresh (< 1h lag) |
### Creative (30%)
| ID | Sev | Pass |
|---|---|---|
| M25 | Critical | ≥ 3 formats active |
| M26 | High | ≥ 5 creatives per ad set (≥ 10 for Advantage+) |
| M27 | High | 9:16 video present |
| M28 | Critical | No active ad with CTR −20% over 14d + frequency > 3 |
| M29 | High | Hook rate ≥ 20–30% (skip < 50% in 3s) |
| M31 | High | ≥ 30% UGC / native |
| M-AN1 | Critical | Concepts genuinely diverse (angles, motivators, people, formats) |
| M-CR1 | High | New concept within 14–21 days |
| M-CR2 | High | Prospecting ad set frequency < 3 (7d) |
| M-CR4 | High | Link CTR ≥ 1% |
### Structure (20%)
| ID | Sev | Pass |
|---|---|---|
| M11 | High | 1–3 campaigns per goal (not fragmented) |
| M12 | High | CBO/ABO fits budget |
| M13 | Critical | < 30% ad sets Learning Limited (Meta: < 20% spend in learning) |
| M14 | High | No needless learning resets (activity log) |
| M17 | High | Each ad set ≥ budget for ~50 events/week (`budget.py min`) |
| M18 | High | Objective matches business goal |
| M33 | Medium | Advantage+ placements unless justified |
| M35 | High | Attribution reviewed post-Jan-2026 |
| M36 | High | Bid strategy sane (no bid cap below historical CPA) |
| M39 | Medium | UTMs on all URLs |
| M40 | Medium | ≥ 1 A/B test or lift test (`ads_experiment_list_tests`) |
| M-ST1 | High | Daily budget ≥ 2–5× target CPA per ad set |
### Audience (20%)
| ID | Sev | Pass |
|---|---|---|
| M19 | High | Ad set overlap < 20% |
| M21 | Medium | Lookalike seeds ≥ 1,000 |
| M22 | Medium | Advantage+ Audience used/tested |
| M23 | High | Purchasers excluded from prospecting (custom-audience exclusions) |
| M24 | High | First-party list uploaded & fresh (with legal basis) |
### Compliance (scored inside Structure)
| ID | Sev | Pass |
|---|---|---|
| C01 | Critical | Special Ad Category declared when applicable |
| C02 | High | No policy-lint HIGH findings on active copy |
| C03 | Medium | AI disclosure decided for AI media |

## Scoring
`score = Σ(points × severity × category) / Σ(possible × severity × category) × 100`; PASS = 1, WARNING = 0.5, FAIL = 0, NA excluded. Severity: Critical 5, High 3, Medium 1.5, Low 0.5. Grades: A ≥ 90, B 75–89, C 60–74, D 40–59, F < 40. Quick win = Critical/High FAIL fixable in < 15 min.
