# Account structure, testing, scaling, kill rules

[OF] = Meta official · [PR] = practitioner heuristic (use as defaults, say so).

## Meta's Performance 5 [OF]
1. **Simplify the account** — fewer campaigns/ad sets; keep <20% of spend in learning (Meta cites up to 68% lower cost per purchase).
2. **Diversify creative** — many genuinely different concepts (Meta cites +32% efficiency, +9% incremental reach).
3. **Conversions API** alongside the pixel.
4. **Creator / partnership content.**
5. **Validate results** — lift tests / incrementality.
Hub: facebook.com/business/ads/performance-marketing

## Learning phase
- ~50 optimization events per ad set in 7 days to exit [OF concept]. Resets on: budget change >~20%, bid strategy change, targeting change, adding/removing ads, new optimization event, pausing >7 days [PR].
- Min daily budget per ad set: `(target CPA × 50) / 7` → `scripts/budget.py min --cpa X` [PR].
- Can't afford it → optimize for a cheaper/higher-funnel event, consolidate to 1 ad set, or accept "Learning Limited" knowingly.

## Structures
| Stage | Structure | Budget |
|---|---|---|
| **Starter (< ~R$100 / US$30 per day)** | 1 CBO campaign · 1 ad set (broad, Advantage+) · 3–5 distinct ads | All in one ad set |
| **Testing** | Separate testing campaign: ABO 1-3-3 (1 campaign, 3 ad sets, 3 ads) or 3:2:2 flexible ad (3 creatives × 2 primary texts × 2 headlines) | Each test gets 2–3× target CPA before judging |
| **Scaling** | Consolidated CBO/Advantage+ campaign; move winners in with the **same post ID** (keeps social proof) | Raise 15–20% every 48–72h (vertical) or add concepts (horizontal) |
Budget split by phase (borghei paid-ads, MIT) [PR]: testing 40/40/20 → optimization 60/25/15 → scaling 70/20/10 (proven / iteration / new tests).

## Kill / keep / scale rules [PR — coinis, admanage, claude-ads]
**Don't judge CPA in the first 48h.** Use the rule that fires first:
| Signal | Threshold | Action |
|---|---|---|
| Spend with 0 conversions | ≥ 3× target CPA | Pause ad |
| CTR (link) | < 0.5% after ~1,000 impressions | Pause / rework hook |
| Hook rate (3s views / impressions) | < 20% after ~2,000 impressions | New first 3 seconds |
| Hold rate (ThruPlay / 3s views) | < 25% | Tighten middle |
| CPC | ≥ 3× account average | Pause |
| CPA | ≤ target for 3+ days with ≥ 10 conversions | Scale +15–20% |
| ROAS | ≥ 1.25 × breakeven ROAS | Scale |
| Fatigue | CTR −30% from peak, prospecting frequency > 2.5–3, CPM +40% vs baseline | Refresh creative |
| Retargeting frequency | > 5–8 / 7 days | Expand pool / refresh |

Reference CTR (link): ~1% OK, 1.5% average, >2% strong direct-response [PR].

## Scaling
- **Vertical**: +15–20% budget every 48–72h while CPA holds (`scripts/budget.py ladder`).
- **Horizontal**: new concepts / new angles / new awareness levels into the winning campaign.
- **Cost cap**: 10–25% above target CPA when spend must be protected [PR].
- Never duplicate an ad set just to "reset" — it competes with itself.

## Naming convention
`<Brand> | <Objective> | <Audience> | <YYYY-MM>` (campaign) · `<Brand> | <Geo/Audience> | <Goal>` (ad set) · `<Brand> | <Format> | <Angle> | <Awareness> | v<n>` (ad). Example: `Acme | SALES | BR-Broad | 2026-10`, `Acme | VID9x16 | SaveTime | ProblemAware | v1`.
