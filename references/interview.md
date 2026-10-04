# The grill — interview design tree

Technique: Matt Pocock's `grilling` (rounds over a design tree). Question bank: Digitizers' 23 intake questions + brag's 9-question rubric + traffic-manager onboarding briefs + Hormozi/Schwartz (see [offer-and-awareness.md](offer-and-awareness.md)).

## How to run it
1. **Frontier = every question whose prerequisites are settled.** Ask the whole frontier in one round, each with your recommendation — via the native question tool when the harness has one (see SKILL.md Phase 2), else as numbered text with ➡️. Wait.
2. Skip anything already answered by: the repo read, `ads/product-context.md`, the MCP context (Phase 0), or earlier answers.
3. **Never ask facts you can look up** (account, Page, pixel, past CPA, competitors). Look them up, then show what you found.
4. Recommendations must be concrete ("R$40/day CBO, 1 ad set, Brazil 18–55, Advantage+") — never "it depends".
5. Push back on weak answers (grill!): vague audience, no margin known, "everyone is my customer", budget too small for the goal. Explain the consequence and recommend a fix.
6. End: summarize the whole tree in a table, ask "Is this our shared understanding?" Only then go to Phase 3.

## The tree (rounds are typical, not fixed)

### Round 1 — Business & goal (no prerequisites)
| # | Question | Why it matters / what to push on |
|---|---|---|
| Q1 | **What exactly are you selling?** (product/service, price, what the buyer gets) | Must fit in one sentence |
| Q2 | **What business result do you want from ads?** sales / leads / messages / app installs / signups / community joins / awareness | Drives objective. Push for ONE primary result |
| Q3 | **Where does the sale/conversion actually happen?** website checkout, WhatsApp/DM chat, phone, lead form, app, physical store | Drives destination |
| Q4 | **What's success in numbers?** target cost per result, monthly volume, or ROAS | If unknown → compute from margin in Round 2 |
| Q5 | (only if >1 account/Page found) **Which ad account / Page / IG?** | Recommend the BM account with payment + history |

### Round 2 — Economics (needs Q1–Q4)
| # | Question | Notes |
|---|---|---|
| Q6 | **Gross margin per sale** (price − cost − fees − shipping) or average deal value | Breakeven ROAS = 1 / margin% (`scripts/roi.py breakeven`) |
| Q7 | **Lifetime value / repeat purchase?** | Lets target CPA exceed first-order margin |
| Q8 | **Budget: daily or total? amount? how long?** | NEVER infer. Run `scripts/budget.py min --cpa X` and show if it's enough |
| Q9 | **Deadline or promo window?** (launch, sale, event) | Urgency + lifetime budget option |

### Round 3 — Customer & offer (needs Q1–Q3)
| # | Question | Notes |
|---|---|---|
| Q10 | **Who buys today?** (best 3 customers: age, situation, trigger moment) | Advantage+ uses this as creative signal, not targeting |
| Q11 | **What do they already know?** (awareness level: unaware → most aware) | Picks ad angle; see Schwartz table |
| Q12 | **Main pain / desire and #1 objection** | Feeds hooks and FAQs |
| Q13 | **Why you vs alternatives?** (mechanism, proof, guarantee, price) | No proof → plan to collect it |
| Q14 | **The offer**: discount, bonus, free trial, guarantee, scarcity? | Score with the value equation |
| Q15 | **Region(s), language(s)**; any location to exclude? | Geo targeting |
| Q16 | **Customer list to use for lookalike or exclusion?** (size, consent) | LGPD/GDPR gate |

### Round 4 — Assets & tracking (needs Q2–Q3)
| # | Question | Notes |
|---|---|---|
| Q17 | **What creative do you have?** photos, videos, UGC, testimonials, brand kit | If `--repo` was used, propose video generation; otherwise ask for media or offer a UGC script |
| Q18 | **Who can appear on camera?** (founder/customers/creators) | UGC beats polished |
| Q19 | **Destination URL / WhatsApp number / form fields** | Check page speed (<3s) and message match |
| Q20 | **Tracking**: pixel on site? CAPI? thank-you page event? CRM? | If missing, recommend minimum fix or a non-pixel objective |
| Q21 | **Restricted category?** health, finance, employment, housing, politics, alcohol, gambling, supplements | Policy + special categories |
| Q22 | **Tone/voice** (and words never to use) | Copy |
| Q23 | **Any AI-generated media?** → disclosure choice | `self_ai_disclosure` |

### Round 5 — Strategy confirmations (after viability research)
| # | Question |
|---|---|
| Q24 | Pick objective/destination option (A/B/C from viability table) |
| Q25 | Approve concepts (3–5) and which to drop |
| Q26 | Approve kill/scale rules and review dates |
| Q27 | Approve the build plan → create as draft |

## Repo-mode shortcuts (`--repo` only)
If `read-repo.md` ran, prefill Q1, Q3 (partially), Q12–Q14, Q17, Q19, Q22 from the code and ask only: "I inferred X — correct?" in one round.

## Push-back library
| Weak answer | Grill response |
|---|---|
| "Everyone is my customer" | "Then the creative decides who. Who are your 3 best customers and why did they buy?" |
| "I don't know my margin" | "Without it we can't know if a sale at cost X is profit. Give me price and unit cost, I'll compute it." |
| Budget < min viable | "At this budget the algorithm can't exit learning for <goal>. Options: optimize for a cheaper event, one ad set only, or raise to Y." |
| "Send to my homepage" | "Homepage = leak. Which page has one action matching the ad promise?" |
| "Make it look professional" | "Polished studio ads usually lose to native/UGC on Meta. Can someone film 30s on a phone?" |
| "Target interest X" | "Interest targeting is now only a suggestion under Advantage+. The creative is the targeting." |
