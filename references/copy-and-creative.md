# Copy & creative

Sources: brag creative laws (MIT), Digitizers creative reference (MIT-0), claude-ads Meta checks (MIT), Meta Andromeda/Performance 5 [OF], ai-ads-claude hooks (MIT).

## Andromeda: creative is the targeting [OF concept]
Meta's retrieval engine narrows millions of ads to a few thousand per person. Near-identical ads get grouped and act as one. → **3–5 (starter) to 10–15 (scale) genuinely different concepts**: different angle, motivator, awareness level, format, person on screen. Color/word swaps are not new concepts. (Exact "similarity %" figures online are unverified — don't cite them.)

## Concept card (one per concept)
| Field | Content |
|---|---|
| Name | `<Brand> \| <Format> \| <Angle> \| <Awareness> \| v1` |
| Awareness level / motivator | from [offer-and-awareness.md](offer-and-awareness.md) |
| Hook (0–3s / first line) | ≤ 8 words, specific |
| Primary text — short | ≤ 125 chars (fits before "…more") |
| Primary text — long | 3–6 short lines, for the 3:2:2 test |
| Headline ×2 | direct + benefit, ≤ 40 chars |
| Description | ≤ 30 chars (often hidden) |
| CTA | from the MCP enum |
| Media | spec below |
| Proof | number / testimonial / demo |

## Laws (from brag, adapted)
- **Hook is everything** — first 2–3s / first line decides. Plan it before anything else.
- **Specific** — feels made for this exact product; numbers > adjectives.
- **Show the thing** — real UI/product in use, not stock.
- **No generic marketing language** — "Streamline your workflow", "game-changer", "revolutionary" are banned.
- **Readable** — sound-off captions; text holds long enough to read.
- Hook speaks to "you", not "we" — but **never asserts personal attributes** (see policy).

## Frameworks by funnel
| Stage | Framework | Shape |
|---|---|---|
| Cold | AIDA | Attention → Interest → Desire → Action |
| Problem-aware / warm | PAS | Problem → Agitate → Solution |
| Retargeting | BAB | Before → After → Bridge |
| Proof-led | "Result first" | Outcome → how → proof → CTA |

## Hook types (generate ≥ 5, pick 3)
Problem call-out · Bold specific result · Curiosity gap · Pattern interrupt (visual) · Social proof first · "Stop doing X" · Demo-in-2-seconds · Price/offer shock · Comparison · Founder story line.

## Media specs
| Placement | Ratio | Size | Notes |
|---|---|---|---|
| Feed (FB/IG) | 4:5 | 1080×1350 | Preferred over 1:1 |
| Stories / Reels | 9:16 | 1080×1920 | Keep text out of top ~14% / bottom ~20% |
| Universal fallback | 1:1 | 1080×1080 | |
| Video length | | 9–20s Reels/Stories; ≤ 30s feed | Hook ≤ 3s, captions always |
| Formats in account | | ≥ 3 (image, video, carousel) | claude-ads M25 |
| UGC share | | ≥ 30% of creatives | claude-ads M31 |
| Refresh | | new concept every 14–21 days | claude-ads M-CR1 |

## Creative sources (pick in this order)
1. User's real photos/videos/testimonials.
2. Repo-generated video ([video-brag.md](video-brag.md)).
3. Screenshots from the repo's `public/` (real UI).
4. UGC brief for a creator/founder ([assets/video-script.template.md](../assets/video-script.template.md)).
5. Static image the user hosts at a public URL. (Image generation tools, if available in the session, → AI disclosure question.)

## Before upload
Run `python <skill-dir>/scripts/policy_lint.py --file copy.txt` (or `--text "..."`). Fix every HIGH; justify or fix MEDIUM.
