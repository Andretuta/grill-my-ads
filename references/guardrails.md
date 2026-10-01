# Guardrails (non-negotiable)

Base: Digitizers/meta-ads-mcp (MIT-0), corrected for the current official MCP + Meta's Performance 5.

## Money
| Rule | Why |
|---|---|
| Everything is born **draft/PAUSED** | Zero spend before review |
| **Publish only on explicit "ok"** in chat, naming what will go live and the spend/day | Approval is per action; an earlier "ok" doesn't cover a new publish |
| **Never infer budget.** "2,000/month" is neither daily nor lifetime → ask which | The MCP's own rule |
| Budget changes **≤ 20%** at a time, 48–72h apart | More resets the learning phase |
| Suggest an **account spending limit** (billing settings) | Caps runaway spend |
| Don't touch an ad set in **learning** (~50 events / 7 days) without a strong reason | Edits restart learning |
| Never change audience + creative + budget at once | Isolate the variable |

## Objects
| Rule | How |
|---|---|
| **Pause, never delete** | `ads_update_entity status=PAUSED`. Deleting loses optimization history |
| Deletes (`ads_creative_delete`, `ads_delete_custom_audience`, `ads_catalog_*delete*`) | Only on an explicit user request for that object |
| Verify after create/edit | `ads_get_ad_entities` with the ID + `effective_status` |
| Preview before publish | `ads_get_ad_preview` + clickable `preview_url` |
| Log every change | In `ads/briefs/...md` (decision log) |

## Targeting & data
- Never invent interest IDs (real numeric IDs, 13–16 digits). No verified ID → broad targeting (geo + age) with Advantage+.
- Declare a **Special Ad Category** when applicable (financial, employment, housing, politics/social issues). Undeclared = rejection and account risk.
- Customer lists: documented legal basis (LGPD/GDPR/CCPA), **SHA-256 hash** (email lowercased/trimmed; phone E.164), minimum fields, honor opt-outs. No sign-off from whoever owns privacy → don't upload.
- Never put personal data in URLs/UTMs.

## Content
- Run `scripts/policy_lint.py` ([policy-and-compliance.md](policy-and-compliance.md)) on all copy.
- `self_ai_disclosure`: always ask; the advertiser decides.
- Nothing secret leaves the repo: keys, tokens, internal hosts, real names/emails → swap for fictional stand-ins and say so.

## Account
- Prefer a Business Manager ad account over a personal one.
- New account: verify identity/business first, start low and ramp (warm-up).
- Rejected ad: read the reason before resubmitting; never resubmit identical creative repeatedly.
- Restricted account: point to the official channel (Account Quality / Meta support). Never work around it (cloaking, serial new accounts).

## Behavior
- Facts → look up (MCP/web). Decisions → ask.
- Market numbers are **ranges** (tag [PR] practitioner vs [OF] official). Never promise a CPA/ROAS.
- If a tool doesn't exist in the MCP, say it can't be done here (don't invent).
