# Ad video from the repo (brag pipeline)

Uses **latent-spaces/brag** (MIT, © 2026 Shunit Haviv Hakimi) — it reads the project and renders a 15–25s video with Hyperframes. grill-my-ads drives it with ad-specific direction; brag owns composition/rendering.

## 1. Check dependencies (facts — look them up, don't ask)
| Need | Check | If missing |
|---|---|---|
| brag skill | Skill list has `brag` or `brag-slim`; or `~/.claude/skills/brag/SKILL.md` exists | Offer to install (ask first): `/plugin marketplace add latent-spaces/brag` then `/plugin install brag@brag` — or `npx skills add https://github.com/latent-spaces/brag --skill brag -g` — or copy `skills/brag/` from a clone into `~/.claude/skills/brag/` (Windows: copy, symlinks often fail) |
| Node ≥ 18 + npx | `node --version` | Ask user to install Node LTS |
| ffmpeg | `ffmpeg -version` | Ask user to install; without it skip poster baking + aspect re-cut |
| Hyperframes | `npx hyperframes --version` (downloads on first run — ask before) | — |

If anything blocks: fall back to user media, a static image, or a UGC script ([assets/video-script.template.md](../assets/video-script.template.md)).

## 2. Run brag with ad direction
Invoke the brag skill (Skill tool) with:
```
/brag --format vertical --duration 15 --tone <mapped> 
Direction for a Meta ad (not a launch post): hook = <winning hook from the grill> in the first 2s, 
show <the key user flow beat>, end card = <offer> + "<CTA text>". Big readable captions (sound-off viewing), 
keep text inside the central 4:5 safe area so the same video can be cropped for feed. 
No secrets, real customer names or internal URLs on screen.
```
Tone mapping: direct-response/clean → `app-store`; premium → `polished`; playful product → `default`; bold/young → `chaotic`.

## 3. Ad-specific acceptance (beyond brag's own gates)
| Check | Rule |
|---|---|
| Hook | Product/benefit visible by 2s; first frame isn't a fade/blank |
| Length | 9–20s for Reels/Stories; ≤ 30s feed |
| Captions | Every spoken/claimed line is on-screen text (≥ 80% watch muted) |
| Safe zones (9:16, 1080×1920) | Keep key text out of top ~14% and bottom ~20% (UI overlays) |
| Feed version | Make 4:5 (1080×1350): re-render `--format square`-like or crop with ffmpeg: `ffmpeg -i brag.mp4 -vf "crop=1080:1350:0:285" brag-4x5.mp4` |
| Policy | Run `scripts/policy_lint.py` on all on-screen text |
| AI disclosure | Video is synthetic/AI-assisted → surface `self_ai_disclosure` choice |

## 4. Upload & use
1. `ads_creative_upload_media` (LOCAL_FILE if supported; else the user hosts the mp4 at a direct public URL).
2. Poll `ads_get_ad_videos` until `ready`.
3. `ads_create_creative` with `placement_videos`: 9:16 for `instagram_positions:["story","reels"]` + `facebook_positions:["story","facebook_reels"]`, 4:5 as fallback (no platforms). Thumbnail: brag's `brag.jpg`.
4. Use brag's `share-copy.txt` only as a draft — rewrite into ad copy per [copy-and-creative.md](copy-and-creative.md).
