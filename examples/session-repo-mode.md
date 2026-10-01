# Example: repo mode + generated video

Fictional repo: `snapinvoice/`, a Next.js app that turns a photo of a receipt into an invoice.

**User:** /grill-my-ads

**Claude:** ❓ I found a project here (`snapinvoice`, Next.js). Can I read the files to build the ad from the real product?
➡️ Recommend yes. It cuts the interview in half. I skip `.env`, keys and build output.

**User:** sim

**Claude (after read-repo.md)**: Here's what I took from the code:

| Field | Inferred | Source |
|---|---|---|
| One-liner | "Photo of a receipt → ready-to-send invoice in 10 seconds" | `app/page.tsx` hero |
| Offer | Free 14-day trial, then US$9/month | `app/pricing/page.tsx` |
| Flow | upload photo → fields auto-filled → "Send invoice" | `components/Uploader.tsx`, `app/invoice/[id]` |
| Conversion | `/signup` → `fbq('track','CompleteRegistration')` | `app/signup/page.tsx` |
| Brand | `#0F172A` / `#22C55E`, Inter | `tailwind.config.ts` |
| Proof | "12,000 invoices sent" | `app/page.tsx` |

**Round 1 (confirm inferences + gaps)**

❓ **Q1** - **Inferences**: is everything above correct? Is "12,000 invoices" current and provable?

➡️ Keep the 12k claim only if you can show it on request. Otherwise use "thousands".

---

❓ **Q2** - **Result**: trial signups (CompleteRegistration) or paid conversions?

➡️ Trial signups. That gives enough events to exit learning; we'll measure paid conversions with `/grill-my-ads roi`.

---

❓ **Q3** - **Creative**: do you have video? If not, I can render a 15s 9:16 product video from the repo (brag pipeline: Node + ffmpeg).

➡️ Generate it. A real-UI demo with the hook "Receipt photo → invoice in 10s" fits the product.

**…grill continues; then Phase 4 runs video-brag.md:**
```
/brag --format vertical --duration 15 --tone app-store
Direction for a Meta ad: hook = "Receipt photo → invoice in 10s" in first 2s, show upload → auto-filled
fields → Send, end card = "Free 14 days" + "Start free". Big captions, text in central 4:5 safe area.
No real customer names or internal URLs on screen.
```
→ `brag-output/brag.mp4` (9:16) + `ffmpeg … crop=1080:1350` → `brag-4x5.mp4` → upload → `placement_videos`.
