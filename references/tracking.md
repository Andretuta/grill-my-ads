# Tracking: UTMs, pixel, CAPI, attribution

## UTMs (`scripts/utm.py`)
Standard template (Meta fills the macros at delivery):
```
utm_source=facebook&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_term={{adset.name}}&utm_content={{ad.name}}&utm_id={{campaign.id}}&placement={{placement}}
```
Names are captured at publish time → name objects right before publishing. Never put personal data in URLs. [PR admanage]

## Pixel & CAPI
| Item | Target | Tool |
|---|---|---|
| Pixel on all pages + standard events (Purchase, Lead, AddToCart, InitiateCheckout, CompleteRegistration) | Firing | `ads_get_datasets`, `ads_get_dataset_stats` |
| Conversions API alongside pixel | Active | `ads_get_dataset_details` |
| Deduplication | Same `event_id` from pixel + CAPI; ≥ 90% dedup | `ads_get_dataset_quality` |
| Event Match Quality | ≥ 7 (Purchase ≥ 8.5 ideal); email-only ≈ 5–6, add phone/name/external_id | `ads_get_dataset_quality` |
| Domain verified, AEM top events prioritized | Done | Business Manager |
| Offline / CRM conversions | Via CAPI with `action_source=physical_store` / `system_generated` (standalone Offline Conversions API discontinued May 2025) [OF] | — |
| Messaging conversions | CAPI for Business Messaging — needs official WhatsApp Business Platform | — |

## Attribution [OF]
- Default: 7-day click + 1-day view. **7-day view and 28-day view windows were removed 12 Jan 2026**; remaining: 1d/7d/28d click, 1d engaged-view, 1d view.
- Don't compare pre-2026 vs post-2026 conversion counts like-for-like (reported conversions dropped for many advertisers [PR]).
- Data retention in Insights API: unique-count & hourly 13 months; frequency breakdowns 6 months; aggregates 37 months.
- Meta-reported ≠ real. ROI uses the business's own data ([roi.md](roi.md)).
