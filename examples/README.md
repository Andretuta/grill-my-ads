# Examples

| File | Shows |
|---|---|
| [session-create.md](session-create.md) | Full `/grill-my-ads` run: context → rounds (❓/➡️) → push-back on budget → viability table → plan → MCP calls → preview → publish gate |
| [session-repo-mode.md](session-repo-mode.md) | Opt-in `--repo` mode: inferences table, video generation with brag |
| [roi/](roi/) | `meta.csv` + `biz.csv` → `expected-output.md` from `roi.py report --margin 0.49 --tax 0.1215` |
| [audit/](audit/) | `checks.json` → `expected-output.md` from `audit_score.py` |
| [copy.txt](copy.txt) | 3 ads → [policy-lint-output.txt](policy-lint-output.txt) from `policy_lint.py --file` |

All brands, IDs and numbers are fictional.

Regenerate from the skill root:
```bash
python scripts/roi.py report --meta examples/roi/meta.csv --biz examples/roi/biz.csv --margin 0.49 --tax 0.1215
python scripts/audit_score.py examples/audit/checks.json
python scripts/policy_lint.py --file examples/copy.txt
```
