# Viability tree: business goal → objective → destination

Valid combos come from the MCP's `ads_create_ad_set` schema (authoritative). Always present 2–3 options + one recommendation.

## Decision table
| Business goal | Objective | optimization_goal | destination_type | CTA | Requirements | When to pick |
|---|---|---|---|---|---|---|
| Online sales (checkout on site) | `OUTCOME_SALES` | `OFFSITE_CONVERSIONS` (Purchase) / `VALUE` | `WEBSITE` | `SHOP_NOW` / `BUY_NOW` | Pixel + Purchase event (+ CAPI ideal); budget ≈ (CPA×50)/7 | Pixel has ≥ some purchase history; budget fits |
| Online sales, low budget / no purchase data | `OUTCOME_SALES` or `OUTCOME_LEADS` | `OFFSITE_CONVERSIONS` on a higher event (AddToCart / InitiateCheckout / Lead) | `WEBSITE` | `SHOP_NOW` | Pixel with that event | Purchase volume too low to exit learning |
| Catalog e-commerce | `OUTCOME_SALES` | `OFFSITE_CONVERSIONS` / `VALUE` | `WEBSITE` | `SHOP_NOW` | Catalog + product set + pixel | Many SKUs (`ads_catalog_*`) |
| Sales that close in chat | `OUTCOME_ENGAGEMENT` or `OUTCOME_LEADS` or `OUTCOME_SALES` | `CONVERSATIONS` (or `MESSAGING_PURCHASE_CONVERSION` if eligible) | `WHATSAPP` / `MESSENGER` / `INSTAGRAM_DIRECT` | `WHATSAPP_MESSAGE` / `MESSAGE_PAGE` | Page + linked WhatsApp Business number; someone/bot answering fast | Local business, high-touch sale, Brazil/LatAm/India |
| Leads (B2B, services) | `OUTCOME_LEADS` | `LEAD_GENERATION` / `QUALITY_LEAD` | (instant form) | `SIGN_UP` / `GET_QUOTE` / `APPLY_NOW` | Lead ToS accepted on Page; CRM to follow up | Fast follow-up exists; no landing page |
| Leads on site | `OUTCOME_LEADS` | `OFFSITE_CONVERSIONS` (Lead) | `WEBSITE` | `SIGN_UP` / `LEARN_MORE` | Pixel Lead event on thank-you page | Qualified landing page exists |
| Traffic (content, community join, no pixel) | `OUTCOME_TRAFFIC` | `LANDING_PAGE_VIEWS` (better than `LINK_CLICKS`) | `WEBSITE` | `LEARN_MORE` / `SIGN_UP` | Fast page | No conversion tracking possible; cheap clicks wanted |
| Followers / profile visits | `OUTCOME_TRAFFIC` / `OUTCOME_ENGAGEMENT` | `PROFILE_VISIT` / `VISIT_INSTAGRAM_PROFILE` / `PROFILE_AND_PAGE_ENGAGEMENT` | `INSTAGRAM_PROFILE` / `FACEBOOK_PAGE` | — | IG/Page | Creator / brand-building |
| Video views / warm audience building | `OUTCOME_ENGAGEMENT` or `OUTCOME_AWARENESS` | `THRUPLAY` | `ON_VIDEO` | — | Video | Cheap TOFU to retarget later |
| Post boost / social proof | `OUTCOME_ENGAGEMENT` | `POST_ENGAGEMENT` | `ON_POST` | — | Existing post | Seeding proof before launch |
| Reach / awareness | `OUTCOME_AWARENESS` | `REACH` / `AD_RECALL_LIFT` | — | — | — | Local reach, events, brand |
| App installs | `OUTCOME_APP_PROMOTION` | `APP_INSTALLS` / `IN_APP_VALUE` | `APP` | `INSTALL_MOBILE_APP` | App registered + SDK | Mobile app |
| Calls | `OUTCOME_TRAFFIC` / `OUTCOME_LEADS` | `QUALITY_CALL` | `PHONE_CALL` | `CALL_NOW` | Phone answered | Emergency/local services |

## Known limitations (tell the user)
- **WhatsApp group invite links can't be an ad destination** and are blocked in lead-form destinations. Pattern: Click-to-WhatsApp to a business number → auto-reply sends the group link; or traffic to a page/short link that redirects to the group (then Meta only optimizes for clicks/LPV). [PR]
- CAPI for messaging (sending purchase/lead events from WhatsApp back to Meta) needs the **official WhatsApp Business Platform**, not unofficial libraries.
- Conversations started from Click-to-WhatsApp ads get a **72h free messaging window** [OF].
- `OUTCOME_SALES` + WEBSITE without a pixel is rejected.
- Since 2026 legacy Advantage+ Shopping/App campaign APIs are gone; Advantage+ = CBO + Advantage+ audience + no placement restrictions (`advantage_state_info`) [OF].

## How to research viability (Phase 3)
1. `ads_library_search` for 3–5 competitors / niche keywords: which destination and format do long-running ads use?
2. Web search: "<niche> meta ads <country> <year> cost per lead/benchmark".
3. MCP facts: pixel present? events firing (`ads_get_dataset_stats`)? lead ToS? IG linked? WhatsApp number on Page?
4. Budget fit: `scripts/budget.py min --cpa <expected CPA from benchmarks>` vs the user's budget.
5. Output table:

| Option | Objective / goal / destination | Expected cost (range, source) | Pros | Cons | Missing |
|---|---|---|---|---|---|
| A (recommended) | … | … | … | … | … |
| B | … | … | … | … | … |
