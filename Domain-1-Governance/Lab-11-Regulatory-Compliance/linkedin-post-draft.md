# LinkedIn Post Draft — Lab 12

---

**Main version**

In late 2016, Uber discovered attackers had accessed data for 57 million riders and drivers. Instead of notifying regulators, the company paid the attackers to delete the data and stay quiet. The breach became public roughly a year later, under new leadership. The resulting multistate settlement — $148 million — wasn't primarily about the breach itself. It was about the concealment and the missed notification deadlines.

That's the pattern most breach post-mortems undersell: regulators consistently penalize delay and concealment harder than the underlying incident, because concealment takes away their ability to protect anyone in real time.

For Lab 12 — the final piece of SAMA CSF Domain 1 in my Saudi Cybersecurity Compliance Labs series — I built the tracker for exactly that failure mode.

**Regulatory Compliance & Multi-Framework Obligations Tracker** (Flask + SQLite, Dockerized, same clean UI as the rest of the series):

→ A **Regulatory Framework Register** — every applicable regulation, each with its own notification deadline: SAMA CSF (2 hours), PDPL (72 hours), NCA ECC, PCI-DSS, SWIFT CSP
→ An **Incident Notification Tracker** — the core mechanic. One incident gets checked against every applicable framework *simultaneously*, each with an independently computed deadline and a live On Time / Late / Pending status
→ A **Compliance Gap Register** that cross-references gaps already surfaced elsewhere in this series — a Cloud Security Policy gap from Lab 06/07, a Critical audit finding from Lab 11 — now mapped to the specific regulation each one violates
→ A **Regulatory Correspondence Log** tracking every formal exchange with SAMA, NCA, or SDAIA against its own due date

I seeded it with a direct replay of the Uber pattern: an incident discovered, handled informally, and only formally reported to SAMA, SDAIA, and PCI-DSS roughly **395 days late** — against deadlines measured in hours, not months. The dashboard doesn't soften that number. It just shows it, next to a clean example where a different incident hit both its applicable deadlines on time.

On-time notification rate across the seeded dataset: 40%. That's not a comfortable number to publish, and that's the point — the whole value of this control is that it can't quietly stay comfortable.

Full code, case study, blank regulatory compliance policy template, and a completed assessment report are on GitHub — link in comments.

#CyberSecurity #GRC #RegulatoryCompliance #SAMA #NCA #PDPL #InfoSec #SaudiArabia #DataProtection #RiskManagement

---
NOTES FOR POSTING (delete before publishing):
- Best visual: screenshot the Notification Tracker showing the Uber-replay incident's "Notified LATE — 394.9d late" pill next to a clean "Notified On Time" pill from a different incident — the contrast makes the point instantly.
- A second image of the Dashboard's framework deadline cards (2h, 24h, 72h side by side) shows the multi-clock complexity visually.
- GitHub link goes in the first comment, not the post body.
