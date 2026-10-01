# Policy & compliance

Official: Meta Advertising Standards — transparency.meta.com/policies/ad-standards/ [OF]. When unsure, `ads_get_help_article` or fetch the policy page; policy beats this summary.

## Copy linter (`scripts/policy_lint.py`)
| Risk | Example (reject) | Fix | Severity |
|---|---|---|---|
| **Personal attributes** — asserting/implying the viewer's health, finances, age, race, religion, sexuality, disability, criminal record, weight | "Are you struggling with anxiety?", "Você está endividado?", "Tired of your belly fat?" | Talk about the product/situation: "A calmer evening routine", "Organize suas dívidas" | HIGH |
| **Guaranteed results / unrealistic claims** | "Guaranteed to lose 10kg", "renda garantida", "100% cure" | "Many customers…", "helps", specifics with proof | HIGH |
| **Before/after** (weight loss, anti-aging) | side-by-side body photos | Show product/process, not bodies | HIGH |
| **Get-rich / investment returns** | "Turn R$100 into R$10,000" | Remove returns promises; financial category | HIGH |
| **Fake urgency/scarcity, fake UI** | fake "play" buttons, fake notifications, "only 2 left" when false | Only real deadlines/stock | MEDIUM |
| **Sensational / shocking** | excessive caps, "!!!", shocking imagery | Calm, specific | LOW–MEDIUM |
| **Restricted goods** | alcohol, supplements, gambling, dating, crypto, pharma, weapons | Check policy + targeting restrictions, age 18+ | MEDIUM |
| **Brand/IP** | competitor logos, "Meta/Facebook/Instagram" in a misleading way, celebrity without consent | Remove | MEDIUM |

## Special Ad Categories [OF]
Declare in `special_ad_categories` **before** creating the campaign when the ad is about:
| Category | Covers | Effect |
|---|---|---|
| `FINANCIAL_PRODUCTS_SERVICES` | credit, loans, cards, insurance, investments | Age 18–65+, all genders, no lookalikes, limited detailed targeting, no ZIP-level |
| `EMPLOYMENT` | job offers, recruiting | same |
| `HOUSING` | rent/sale, mortgages, home insurance | same |
| `ISSUES_ELECTIONS_POLITICS` | social issues, elections, politics | Authorization + "Paid for by" disclaimer required |
Financial advertiser verification is expanding by country (2026) [PR] — check the help center for the target country.

## AI disclosure
- `self_ai_disclosure` on `ads_create_creative`: `OPT_IN` (media created/edited with third-party gen-AI) or `OPT_OUT`. **Always ask; advertiser decides; immutable after creation.**
- Mandatory self-disclosure for social-issue/political ads using realistic AI media [OF]. Meta may auto-label "AI info" from C2PA metadata [PR].

## Privacy (LGPD / GDPR / CCPA)
- The advertiser is responsible for compliance [OF — Meta LGPD help 327111418314780].
- Customer list uploads: legal basis (consent / legitimate interest for active customers), SHA-256 hashing, minimal fields, opt-out honored, privacy policy mentions ad targeting.
- Never send health/financial sensitive data as events or audience sources.

## Account health
| Ban risk [PR] | Prevention |
|---|---|
| Repeated rejections | Lint before submit; never resubmit identical |
| Cloaking / bypassing review | Never |
| Payment failures | Stable payment method; spending limit |
| Logins from many IPs/devices, abrupt changes on a new account | Verify identity/business; ramp budget gradually |
| Links to risky BMs/domains | Verify domain in Business Manager |
If restricted: Account Quality → request review. No workarounds.
