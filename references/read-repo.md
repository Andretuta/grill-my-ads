# Reading the repo to build the ad

Adapted from brag's `step-1-inspect.md` (MIT). **Opt-in only:** run when the user passed `--repo` or explicitly asked to use the project's code. Never on your own initiative.

## Read, in priority order
1. **Landing / marketing page** — `index.html`, `app/page.*`, `pages/index.*`, `src/App.*`: title, hero headline, tagline, section headings, CTAs, testimonials, pricing, FAQ. This is the product's own voice.
2. **Styles** — `:root` CSS vars, Tailwind config, theme files: brand colors, fonts (for creatives/video).
3. **README.md / PRODUCT.md / docs/** — one-liner, features, "how it works", who it's for.
4. **package.json / pyproject / app.json** — name, description, homepage, app store IDs.
5. **Routes & key components** — the real user flow: **entry → key action → result**. The strongest ad material is the product *in use*.
6. **Pricing / plans / checkout code** — price points, trials, guarantees (offer facts).
7. **public/ assets/** — logos, screenshots, product images, demo videos (candidate creatives).
8. **Analytics/tracking code** — Meta pixel (`fbq(`), GA4, UTMs, CAPI endpoints, thank-you pages → feeds Q20 and [tracking.md](tracking.md).
9. **Existing ad/marketing folders** — `ads/`, `marketing/`, previous briefs, `ads/product-context.md`.

## Never read
Build output (`dist/`, `.next/`, `build/`), lock files, `.git/`, `node_modules/`, tests, `.env*`, keys/certs (`*.pem`, `*.key`, `id_rsa`, service-account JSON), `secrets/`, `credentials/`, auth/session folders, anything `.gitignore` excludes for secrecy.

## Rule: nothing secret leaves this step
Everything read may end up in public copy or video. Never carry API keys, tokens, internal hostnames/URLs, real customer names, emails, phone numbers, or any personal data into the context file, copy, or video. Use fictional stand-ins and say so.

## Output: prefill `ads/product-context.md`
Fill [assets/product-context.template.md](../assets/product-context.template.md) and mark each field `(from repo: <file>)` or `(needs confirmation)`. Then answer the brag rubric adapted for ads:

| # | Question |
|---|---|
| 1 | What is it, in one sentence a stranger gets? |
| 2 | The most impressive/specific claim on the site (a number beats an adjective) |
| 3 | The visual hook (UI moment, before/after state, result screen) |
| 4 | Which real UI to show in the ad |
| 5 | Who is it obviously for (from copy/pricing/features)? |
| 6 | The offer visible in code (trial, discount, free tier, guarantee) |
| 7 | Where conversion happens (checkout, signup, WhatsApp link, form, app store) and is it tracked? |
| 8 | Tone of the existing copy |
| 9 | The user flow worth showing: entry → key action → result |

Bring these to the grill as "I inferred X — correct?" questions in a single round.
