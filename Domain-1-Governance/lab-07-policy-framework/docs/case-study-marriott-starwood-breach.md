# Case Study: The Marriott / Starwood Breach (Disclosed 2018)

*This account is compiled from widely reported public facts about the incident, summarized in the author's own words for educational use in this lab.*

## Timeline
1. **2014 (approximately)** — Unauthorized access begins on Starwood Hotels & Resorts' guest reservation database, according to Marriott's later investigation.
2. **September 2016** — Marriott International completes its acquisition of Starwood, becoming one of the largest hotel companies in the world, combining loyalty programs, reservation systems, and IT estates.
3. Starwood's reservation systems continue operating for an extended period following the acquisition, reportedly without being fully brought under a harmonized, unified security policy framework in the immediate aftermath of the deal.
4. **September 2018** — An internal security tool flags a suspicious attempt to access the Starwood guest reservation database, triggering an investigation.
5. **November 2018** — Marriott publicly discloses the breach, revealing that unauthorized access had likely existed since 2014 — meaning the intrusion **predated the acquisition** and continued undetected for roughly four years, spanning the integration period.
6. The exposed data included personal information for approximately **500 million guests**, with some records including passport numbers and payment card data (some encrypted, with reports raising questions about the strength and consistency of encryption practices across the legacy Starwood systems).

## Root cause breakdown (mapped to controls this lab implements)

| # | Root cause | Control that should have existed | Lab implementation |
|---|---|---|---|
| 1 | Starwood's systems weren't promptly harmonized under Marriott's policy framework post-acquisition | A documented M&A security integration policy with a hard, tracked timeline | M&A / Third-Entity Integration Register |
| 2 | No framework-wide gap analysis conducted after the deal closed | A coverage analysis mapping every control domain against every business unit | Coverage Gap Analysis module |
| 3 | Legacy Starwood systems ran under old assumptions for years | Policy inheritance/harmonization tracking with explicit gap notes | Entity register — integration % + gap notes |
| 4 | Intrusion undetected for ~4 years, spanning the acquisition period | Consistent monitoring/logging policy applied uniformly, not just to "core" systems | Coverage Gap Analysis — flags domains (e.g. monitoring) with no current policy |

## Why this matters under SAMA/NCA
- **SAMA CSF 4.2** requires SAMA approval and documented due diligence for critical outsourcing arrangements, plus **exit strategy and transition plans** — the acquisition/integration equivalent of exactly this kind of due diligence.
- **NCA ECC 4‑1** requires **ongoing monitoring** of third-party relationships, not a one-time assessment at the start.
- A mature policy framework isn't just "we have policies" — it's **proof of scope**: which systems, which subsidiaries, which acquired entities are actually covered, and which are still running on old assumptions.

## Discussion questions for your LinkedIn/portfolio writeup
- If your organization acquired another company tomorrow, is there a documented, time-bound plan for extending your policy framework to their systems — or would it happen informally, "eventually"?
- Could you currently produce, on demand, a list of every subsidiary or acquired entity and exactly which of your policies do and don't yet apply to them?
- What's the "Starwood reservation system" in your own environment — a system that's been quietly running under old assumptions since before your current policy framework existed?
