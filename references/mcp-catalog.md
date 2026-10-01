# Official Meta Ads MCP catalog (`https://mcp.facebook.com/ads`)

Tools show up as `mcp__<server-id>__ads_*` (prefix varies per install; match by suffix). If they are deferred, load the schema first (ToolSearch `select:...`). **The loaded schema is the authority** — if this file disagrees, follow the schema.

## Common parameters (every `ads_*`)
| Parameter | Rule |
|---|---|
| `client_conversation_id` | 20 chars `[A-Za-z0-9]`, generated on the first call, repeated on **every** later call. Never an account/campaign ID |
| `advertiser_request` | The user's request **in their own words**, combining the original goal + later confirmation. No personal data |
| `client_model` | Exact model ID if the system states it; otherwise omit |
| `ad_account_id` | Numeric, **without** `act_` |
| Money | **Cents** (smallest currency unit). 30.00/day = `3000` (`scripts/budget.py cents 30`) |
| `hide_ui` | `true` when creating many objects at once |

## Discovery
| Tool | Use / gotcha |
|---|---|
| `ads_get_ad_accounts` | Lists accounts; check `is_queryable` (if false, surface `not_queryable_reason`) |
| `ads_get_pages_for_business` / `ads_get_user_pages` | Available Pages. **Use these** |
| `ads_get_ad_account_pages` | Only Pages already used in ads → empty on new accounts. Carries `leadgen_tos_accepted` |
| `ads_get_ig_accounts`, `ads_get_ig_media` | IG account for `instagram_user_id`; posts to boost |
| `ads_insights_advertiser_context` | Advertiser context (vertical, history) |

## Creation (always PAUSED / draft)
### `ads_create_campaign`
- Required: `ad_account_id`, `campaign_name`, `objective`, `buying_type=AUCTION`.
- `objective` ODAX only: `OUTCOME_AWARENESS | OUTCOME_TRAFFIC | OUTCOME_ENGAGEMENT | OUTCOME_LEADS | OUTCOME_SALES | OUTCOME_APP_PROMOTION`.
- **CBO by default**: `campaign_daily_budget` (or `campaign_lifetime_budget`) in cents. ABO only if the user asks → leave campaign budget/bid empty and set `daily_budget` on the ad set.
- `campaign_bid_strategy` default `LOWEST_COST_WITHOUT_CAP`; `COST_CAP` / `LOWEST_COST_WITH_BID_CAP` only with a validated target CPA.
- `special_ad_categories` (JSON array; `[]` if none) — `FINANCIAL_PRODUCTS_SERVICES`, `EMPLOYMENT`, `HOUSING`, `ISSUES_ELECTIONS_POLITICS`; plus `special_ad_category_country`.
- The response includes `valid_optimization_goals` + `recommended_optimization_goal` → use them on the ad set.
- After creating: verify with `ads_get_ad_entities object_ids=[id] level=campaign fields=[..., effective_status]`.

### `ads_create_ad_set`
- Required: `ad_account_id`, `campaign_id`, `ad_set_name`, `billing_event` (use `IMPRESSIONS`), `optimization_goal`, `targeting` (JSON string).
- Minimal `targeting`: `{"geo_locations":{"countries":["BR"]},"age_min":18}`. **Never invent interest IDs.** Advantage+ Audience is default (age becomes a suggestion; hard cap needs `targeting_automation.advantage_audience=0`).
- Placements: omit = Advantage+ Placements. Manual = `publisher_platforms` + `*_positions` inside `targeting`.
- Under CBO, **don't** pass `daily_budget`, `bid_strategy`, `bid_amount` (rejected).
- Destination × goal pairs (see [objectives-destinations.md](objectives-destinations.md)):
  - `CONVERSATIONS` → `destination_type` = `WHATSAPP` | `MESSENGER` | `INSTAGRAM_DIRECT` (+ `promoted_object.page_id`). Under `OUTCOME_LEADS`, CONVERSATIONS needs WHATSAPP.
  - `LEAD_GENERATION` / `QUALITY_LEAD` → Page with lead ToS accepted (`https://www.facebook.com/legal/leadgen/tos`) + `promoted_object.page_id`.
  - `OFFSITE_CONVERSIONS` / `VALUE` → `promoted_object` with `pixel_id` (+ `custom_event_type`). `OUTCOME_SALES` + WEBSITE without pixel = rejected.
  - `POST_ENGAGEMENT`→`ON_POST`, `PAGE_LIKES`→`ON_PAGE`, `THRUPLAY`→`ON_VIDEO` (under ENGAGEMENT with promoted_object).
  - `PROFILE_VISIT`→`FACEBOOK_PAGE`/`INSTAGRAM_PROFILE`; `VISIT_INSTAGRAM_PROFILE`→`INSTAGRAM_PROFILE`.
- `attribution_spec`: omit (default 7-day click + 1-day view).

### `ads_create_creative`
- Image: `ad_account_id`, `page_id`, `link_url`, `image_hash` **or** `image_url`.
- Video: `video_id` + thumbnail (`image_hash`/`image_url`); `link_url` optional.
- Placement-customized video: `placement_videos` (2–10; exactly one fallback without platforms) — ideal for 9:16 (stories/reels) + 4:5 (feed).
- Static carousel: `cards` (2–10). Catalog: `product_set_id`. Boost post: `object_story_id` (`pageid_postid`). Partnership: `facebook_partnership_ad`.
- Text: `message` (primary), `headline`, `description`, `call_to_action_type` (e.g. `LEARN_MORE`, `SHOP_NOW`, `SIGN_UP`, `WHATSAPP_MESSAGE`, `MESSAGE_PAGE`, `GET_OFFER`, `DOWNLOAD`, `INSTALL_MOBILE_APP`).
- `instagram_user_id` to deliver on IG. `display_link` is immutable.
- `advantage_plus_creative` true/false — ask; since 2026 enhancements default ON for several objectives, review off-brand ones.
- **`self_ai_disclosure` `OPT_IN`/`OPT_OUT`**: always surface it for the advertiser to decide; cannot be changed later.

### `ads_create_ad`
- Required: `ad_account_id`, `ad_set_id`, `ad_name`, `creative` (`{"creative_id":"..."}`) or `source_ad_id`.
- **DRAFT MODE**: returns `status=DRAFT`; nothing exists live until published. Errors in `active_errors`.

## Media
| Tool | Use |
|---|---|
| `ads_creative_upload_media` | `upload_source=LOCAL_FILE` (opens upload app; only if the client supports MCP Apps) or `URL` + `media_type` IMAGE/VIDEO + direct public `media_url` (sign-in Drive/Dropbox links fail) |
| `ads_get_ad_images` / `ads_get_ad_videos` | Status/hash; a video is usable only when `ready` |

## Review
| Tool | Use |
|---|---|
| `ads_get_ad_preview` | `ad_id` **or** `creative_id` (no `ad_account_id`). **Always paste `preview_url`.** Optional `ad_format` (MOBILE_FEED_STANDARD, INSTAGRAM_STANDARD, INSTAGRAM_STORY, INSTAGRAM_REELS, FACEBOOK_REELS_MOBILE…). Fresh draft failed → retry once with `creative_id` |
| `ads_get_creatives`, `ads_get_creative_ads` | Creative inventory |
| `ads_get_opportunity_score` | Meta's recommendations for the account/campaign |

## Publish & edit
| Tool | Use |
|---|---|
| `ads_activate_entity` | **Only on explicit "ok".** Drafts: pass `object_ids` with campaign + ad sets + ads (get them via `ads_get_ad_entities object_state=draft`). `PUBLISHING` ≠ live. `ignore_validation_errors` only if the user saw the errors and said go |
| `ads_update_entity` | Pause (`status=PAUSED`), budget (≤20%), name, dates. Changing a live object = confirm first |
| `ads_creative_update` / `ads_creative_delete` | Edit/remove creative (delete only on explicit request) |

## Reading & metrics
| Tool | Use |
|---|---|
| `ads_get_ad_entities` | Live campaigns/ad sets/ads or `object_state=draft`. Validate `fields` with `ads_get_field_context` first. **If `next_actions` comes back, run the read-only queue in step order before answering** |
| `ads_get_field_context` | Canonical metric names, filters, operators |
| `ads_get_errors` | Errors / rejections |
| `ads_account_get_activity_logs` | Change history (who changed what) |

## Insights
`ads_insights_performance_trend`, `ads_insights_anomaly_signal`, `ads_insights_industry_benchmark`, `ads_insights_auction_ranking_benchmarks`, `ads_insights_advertiser_context` — used by the audit.

## Audiences
`ads_create_custom_audience`, `ads_update_custom_audience`, `ads_update_custom_audience_users` (SHA-256 normalized data, documented legal basis), `ads_get_custom_audience`, `ads_get_ad_account_custom_audiences`, `ads_get_custom_audience_adsets`, `ads_delete_custom_audience` (only on request).

## Pixel / dataset
`ads_get_datasets`, `ads_get_dataset_details`, `ads_get_dataset_quality` (EMQ), `ads_get_dataset_stats`, `ads_get_customconversions`, `ads_pixel_event_create|read|update|delete`, `ads_pixel_parameter_create|read|update|delete`.

## Experiments
`ads_experiment_check_eligibility`, `ads_experiment_abtest_create_test|get_test|update_test`, `ads_experiment_lift_create_test|get_test`, `ads_experiment_list_tests`.

## Catalog (e-commerce)
`ads_catalog_list_catalogs`, `ads_catalog_create`, `ads_catalog_list_products`, `ads_catalog_product_create`, `ads_catalog_update_product`, `ads_catalog_list_product_sets`, `ads_catalog_create_product_set`, `ads_catalog_list_product_feeds`, `ads_catalog_create_product_feed`, `ads_catalog_get_diagnostics`, `ads_catalog_get_dynamic_ads_health`, `ads_catalog_list_dpa_eligible_catalogs`, `ads_catalog_event_source_*`, and other `ads_catalog_*`.

## Research & help
| Tool | Use |
|---|---|
| `ads_library_search` | Ad Library — what competitors run (long-running ad ≈ winner) |
| `ads_get_help_article` | Official Help Center article |
| `ads_boost_ig_post` | Boost an IG post |

## Does NOT exist (don't call)
`ads_catalog_get_catalogs` (it's `ads_catalog_list_catalogs`), `ads_activate_entity(status: PAUSED)` (pausing is `ads_update_entity`), legacy objectives (`TRAFFIC`, `LINK_CLICKS`, `CONVERSIONS`…).
