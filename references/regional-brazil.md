# Regional notes: Brazil (BRL)

Use this when the ad account is in BRL or the audience is in Brazil. For other countries, research the same rows (tax pass-through, payment methods, benchmarks, privacy law, messaging habits) and state sources.

## Taxes on ad spend [OF — Meta notice, Sep 2025]
- From **1 Jan 2026** Meta (Facebook Serviços Online do Brasil) passes **PIS/Cofins (9.25%) + ISS (2.9%) ≈ +12.15%** to advertisers. CBS/IBS 1% is test-only in 2026 (not passed through).
- **Prepaid (Pix/boleto)**: tax deducted upfront → R$100 added ≈ R$88 of media [PR]. **Postpaid card**: billed spend + tax.
- IOF 3.5% only if billed in foreign currency on an international card.
- ROI: real cost = spend × 1.1215 (`scripts/roi.py --tax 0.1215`, default for BRL). Companies may recover part as credit — accountant confirms.

## Benchmarks 2026 [PR — trafius, viniensina; use as ranges only]
| Metric | Range |
|---|---|
| CPM feed | R$15–35 |
| CPM stories/reels | R$8–20 |
| Avg CPC | ~R$1.95 (fashion/beauty ~R$0.95; local services ~R$1.60; real estate ~R$2.10; B2B SaaS ~R$2.80) |
| CPL | courses R$8–30 · clinics R$20–60 · real estate R$30–100 · law R$40–120 |
| Practical min daily budget | ~R$20–50 per ad set to learn; technical floor much lower |
Some published CPC numbers look like CPA — prefer `ads_insights_industry_benchmark` for the account when available.

## Messaging culture
- WhatsApp is the default sales channel → Click-to-WhatsApp often beats landing pages for SMB/local. 72h free window after an ad-initiated conversation [OF]. Marketing template ≈ R$0.25, utility ≈ R$0.06 per message (per-message pricing) [PR].
- WhatsApp **group links** can't be the ad destination → C2WA + auto-reply with link, or traffic to a redirect page.

## LGPD
Advertiser is controller. Customer lists need legal basis + SHA-256; honor deletion requests. [OF Meta LGPD help]

## Account restrictions
~1 in 4 BR advertisers report a restriction in 12 months [PR]. Verify identity/business before launch, warm up new accounts, avoid cloaking and serial rejections, keep payment stable.
