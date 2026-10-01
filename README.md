<p align="center">
  <img src="assets/icon.png" alt="grill-my-ads icon" width="160">
</p>

<h1 align="center">grill-my-ads</h1>

<p align="center">
  <b>A relentless media buyer in your terminal.</b><br>
  A Claude skill that grills you about your product, reads your repo, and builds Meta ads (Facebook · Instagram · WhatsApp · Messenger) through the official Meta Ads MCP — as drafts, published only on your "ok".
</p>

<p align="center">
  <a href="README.pt-BR.md">🇧🇷 Leia em português</a>
</p>

---

## Why

Most ad money is lost before the first impression: wrong objective, no margin math, a homepage as destination, five copies of the same creative. `grill-my-ads` interviews you like a senior media buyer *before* spending a cent, does the research itself, and only then builds the campaign.

## What it does

| Command | What happens |
|---|---|
| `/grill-my-ads` | Grills you in rounds (numbered questions, each with a recommended answer) → optionally reads your repo (with permission) → researches the most viable objective/destination → writes 3–5 genuinely different concepts → generates a product video from your code (via [brag](https://github.com/latent-spaces/brag)) → builds campaign, ad set, creatives and ads **as drafts** → shows previews → publishes **only on explicit "ok"** |
| `/grill-my-ads audit` | Read-only account audit: ~40 checks (pixel/CAPI, creative diversity & fatigue, structure, audience, compliance) → 0–100 score, A–F grade, quick wins |
| `/grill-my-ads roi` | Joins Meta spend with **your** business data (orders, qualified leads, retained members) → real CPA, ROAS vs breakeven ROAS, profit, and a SCALE / KEEP / CUT verdict per ad |

### Highlights
- **Facts it looks up, decisions you make.** Account, Page, IG, pixel, history → fetched via MCP. Budget, offer, approval → asked.
- **Repo → ad.** Reads your landing page, pricing, routes and real user flow; never reads `.env`, keys or secrets.
- **Video creatives.** Uses your media or renders a 9:16 + 4:5 product video from the codebase.
- **Safety first.** Draft/PAUSED by default, pause-never-delete, never infers budget, never invents interest IDs, ≤20% budget steps, policy linter on every line of copy, AI-disclosure always asked.
- **Up to date (2026).** Advantage+ unification, Andromeda creative diversity, Jan-2026 attribution window removal, Brazil's 12.15% ad-tax pass-through, LGPD/GDPR notes.

## Requirements

- [Claude Code](https://claude.com/claude-code) or Claude.ai (Customize → Skills)
- The official **Meta Ads MCP** connected: `https://mcp.facebook.com/ads`
- Python 3.9+ (for the helper scripts, stdlib only)
- Optional, for video: Node 18+, ffmpeg and the [brag](https://github.com/latent-spaces/brag) skill

## Install

**Claude Code**
```bash
git clone https://github.com/Andretuta/grill-my-ads ~/.claude/skills/grill-my-ads
```

**Claude.ai** — download the repo as ZIP and upload it in *Customize → Skills*.

Then just say `/grill-my-ads` (or "grill me about my ad").

## Helper scripts

All stdlib Python, each with `--selftest`.

| Script | Example |
|---|---|
| `scripts/budget.py` | `python scripts/budget.py min --cpa 40` → min daily budget to exit learning, in cents too |
| `scripts/policy_lint.py` | `python scripts/policy_lint.py --file copy.txt` → flags personal attributes, guarantees, before/after… (EN + PT) |
| `scripts/audit_score.py` | `python scripts/audit_score.py checks.json` → weighted score + grade + quick wins |
| `scripts/roi.py` | `python scripts/roi.py report --meta meta.csv --biz biz.csv --margin 0.45 --tax 0.1215` |
| `scripts/utm.py` | `python scripts/utm.py example.com/offer` → standard Meta UTM template |

## Layout

```
SKILL.md              router + create flow + non-negotiable rules
references/           MCP catalog, interview tree, viability tree, creative, policy,
                      tracking, structure & scaling, audit, ROI, regional notes, sources
scripts/              budget · policy_lint · audit_score · roi · utm
assets/               product-context, brief and video-script templates
examples/             full sample sessions + sample inputs/outputs
```

## Examples

See [`examples/`](examples/): a full grill session (with budget push-back and a viability table), a repo-mode session with video generation, plus ROI, audit and policy-lint inputs with expected outputs.

## Disclaimer

Not affiliated with Meta. Benchmarks are ranges tagged as official [OF] or practitioner [PR]; they are not guarantees. You are responsible for your ad spend, policy compliance and privacy obligations. The policy linter is a heuristic, not an approval.

## Credits

Built on ideas from [Digitizers/meta-ads-mcp](https://github.com/Digitizers/meta-ads-mcp) (MIT-0), [claude-ads](https://github.com/Hainrixz/claude-ads) (MIT), [latent-spaces/brag](https://github.com/latent-spaces/brag) (MIT), Matt Pocock's [grilling](https://github.com/mattpocock/skills) technique and others. See [LICENSES.md](LICENSES.md).

## License

[MIT](LICENSE)
