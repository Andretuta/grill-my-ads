# Example session: `/grill-my-ads` (no repo)

Fictional product: **Grão Certo**, a specialty-coffee subscription in São Paulo. IDs are fake. Shows the expected *shape* of each phase.

---

**User:** /grill-my-ads quero anunciar minha assinatura de café

**Claude (Phase 0, after silent MCP lookups):**

📋 **What I already know**
| Item | Found |
|---|---|
| Ad account | `Grão Certo` · 111222333 · BRL · America/Sao_Paulo · queryable ✅ |
| Page / IG | Grão Certo Cafés (444555666) · @graocerto ✅ |
| Pixel | `Grão Certo Pixel` · Purchase firing · EMQ 6.1 (CAPI not active) ⚠️ |
| History (90d) | 1 boosted post, R$300 spent, 0 tracked purchases |

**Round 1**

❓ **Q1** - **What exactly do you sell?**: price, what arrives, how often?

➡️ I see "a partir de R$79/mês" on your Page. Confirm the plans and what's in the box.

---

❓ **Q2** - **Primary result from ads**: (a) subscriptions on the site, (b) WhatsApp conversations, (c) followers.

➡️ (a) Site subscriptions. Your pixel already fires Purchase, so Meta can optimize for actual buyers.

---

❓ **Q3** - **Success in numbers**: what's the most you'd pay per new subscriber?

➡️ Answer after Round 2: we'll derive it from margin × months a subscriber stays.

---

**User:** R$79 e R$129, 250g ou 500g por mês. Assinatura no site. Não sei quanto pagar.

**Round 2**

❓ **Q4** - **Margin**: cost of coffee + packaging + shipping + payment fees on the R$79 plan?

➡️ Typical specialty-coffee subscriptions run ~40–50% contribution margin. Give me the real costs and I'll compute it.

---

❓ **Q5** - **Retention**: how many months does an average subscriber stay?

➡️ If you don't know, check how many of the subscribers from 3 months ago are still active.

---

❓ **Q6** - **Budget**: daily or total, and for how long?

➡️ Run `budget.py min` once we have a target CPA. Expect roughly R$100/day to optimize for Purchase.

---

**User:** custo uns R$40, ficam ~4 meses, posso R$60/dia por 30 dias

**Claude:**
- Margin ≈ (79 − 40) / 79 = 49% → `roi.py breakeven --margin 0.49` → **2.04×** on first order.
- LTV ≈ 4 × R$39 = R$156 → max CPA ≈ R$156. Target CPA **R$60** (keeps LTV:CAC ≈ 2.6, aim for 3).
- `budget.py min --cpa 60` → **R$428/day** to get 50 purchases/week. At R$60/day, the ad set would stay in learning on Purchase. **Push back:**

❓ **Q7** - **Budget vs goal**: R$60/day is ~7× short of exiting learning on Purchase. Options: (a) optimize for InitiateCheckout (cheaper, more events), (b) keep Purchase in 1 ad set and accept Learning Limited, (c) raise the budget.

➡️ (a) for the first 14 days with 1 ad set, then switch to Purchase once you have ≥ 25 purchases/week.

*(Rounds 3–4: customer, offer, assets, tracking … omitted)*

---

**Phase 3: viability (after `ads_library_search "café especial assinatura"` + web research)**

| Option | Objective / goal / destination | Expected CPA [PR] | Pros | Cons | Missing |
|---|---|---|---|---|---|
| **A (recommended)** | OUTCOME_SALES / OFFSITE_CONVERSIONS (InitiateCheckout→Purchase) / WEBSITE | R$40–90 | Optimizes toward buyers; uses existing pixel | Low budget for Purchase | CAPI (EMQ 6.1) |
| B | OUTCOME_ENGAGEMENT / CONVERSATIONS / WHATSAPP | R$8–20 per conversation | Cheap, personal sale | Needs someone answering fast; manual close | WhatsApp Business on Page |
| C | OUTCOME_TRAFFIC / LANDING_PAGE_VIEWS | R$0.50–1.50 per view | Cheapest | Optimizes for clickers, not buyers | — |

Competitors' longest-running ads: UGC "unboxing + first sip" 9:16 videos with a first-box discount.

---

**Phase 5: plan (user approved option A)**

| Item | Value |
|---|---|
| Campaign | `GraoCerto \| SALES \| BR-SP-Broad \| 2026-10` · CBO R$60/day = **6000** cents |
| Ad set | `GraoCerto \| SP+30km \| InitiateCheckout` · 25–55 · Advantage+ audience & placements |
| Ads (3 concepts) | `VID9x16 \| FirstSip \| Unaware` · `IMG4x5 \| PriceVsCafeteria \| SolutionAware` · `CAR \| 3Origins \| ProductAware` |
| URL | `utm.py https://graocerto.com.br/assine` |
| Kill/scale | per brief template |

**User:** pode criar

**Phase 6: MCP calls (abridged; same `client_conversation_id` everywhere)**
```jsonc
// ads_create_campaign
{"ad_account_id":"111222333","campaign_name":"GraoCerto | SALES | BR-SP-Broad | 2026-10",
 "objective":"OUTCOME_SALES","buying_type":"AUCTION","campaign_daily_budget":6000,
 "special_ad_categories":"[]","client_conversation_id":"Q7mK2pX9aB4cD1eF6gH3",
 "advertiser_request":"quero anunciar minha assinatura de café ... pode criar"}
// ads_create_ad_set (no budget/bid: CBO parent)
{"ad_account_id":"111222333","campaign_id":"<cid>","ad_set_name":"GraoCerto | SP+30km | InitiateCheckout",
 "billing_event":"IMPRESSIONS","optimization_goal":"OFFSITE_CONVERSIONS","destination_type":"WEBSITE",
 "promoted_object":"{\"pixel_id\":\"777\",\"custom_event_type\":\"INITIATED_CHECKOUT\"}",
 "targeting":"{\"geo_locations\":{\"custom_locations\":[{\"latitude\":-23.55,\"longitude\":-46.63,\"radius\":30,\"distance_unit\":\"kilometer\"}]},\"age_min\":25,\"age_max\":55}"}
// ads_creative_upload_media → ads_get_ad_videos until ready → ads_create_creative (placement_videos 9:16 + 4:5,
//   self_ai_disclosure:"OPT_OUT" as chosen by the user) → ads_create_ad ×3 (DRAFT)
// ads_get_ad_entities {"object_state":"draft","object_ids":["<cid>"]}  → 0 active_errors
```

**Phase 7: preview**
- Concept 1: [preview](https://www.facebook.com/ads/api/preview_iframe.php?…)
- Concept 2: `<preview_url>` · Concept 3: `<preview_url>` (always paste the real clickable URLs)

**Phase 8: gate**
> Publish these 5 objects (1 campaign, 1 ad set, 3 ads)? Spend starts at **R$60/day + ~12.15% tax** (≈ R$67.29/day).

**User:** ok, publica

```jsonc
// ads_activate_entity
{"ad_account_id":"111222333","entity_id":"<cid>","entity_type":"campaign",
 "object_ids":["<cid>","<asid>","<ad1>","<ad2>","<ad3>"]}
```
→ `PUBLISHING`. "Handed off to Meta's publisher. I'll confirm it's live with `ads_get_ad_entities` in a few minutes. Brief saved to `ads/briefs/2026-10-01-graocerto-sales.md`. Next: `/grill-my-ads audit` on 2026-10-08."
