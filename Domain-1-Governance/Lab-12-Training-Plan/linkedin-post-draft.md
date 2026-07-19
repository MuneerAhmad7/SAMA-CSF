# LinkedIn Post Draft — Lab 13

---

**Main version**

The 2015 OPM breach exposed background-investigation data for over 21 million people — the kind of records collected for security clearances, covering not just federal employees but their families. What stuck with me reading the congressional oversight report afterward wasn't the intrusion technique. It was this: OPM's own Inspector General had been flagging serious technical security capability gaps for years before the breach. The warnings existed. They just never turned into the staffing, training, or certification depth needed to close them.

Most "security training" content on LinkedIn is about phishing awareness for the whole company. That's real and necessary — I built that in Lab 09. But SAMA CSF actually splits this into two separate obligations: general staff awareness, and a distinct, deeper requirement for the security team's own technical training and certifications. Most orgs have the first. Fewer can produce evidence of the second.

Lab 13: **Security Team Training & Certification Plan Tracker** — built specifically for that gap.

→ A **Skills Matrix** — current vs. required competency (0-4 scale) across 6 technical specialties, per team member, visualized so a 2-level gap is impossible to miss
→ A **Certification Register** with automatic expiry monitoring — Active, Expiring Soon, or Expired, flagged the same way you'd track a domain certificate
→ A **funded, dated Training Plan** — because a skill gap without a budget and a target date is just a documented excuse

I seeded it with a direct replay of the OPM pattern: a Critical, 2-level Digital Forensics gap on the SOC team, already flagged in an internal audit finding — cross-referenced against a Critical audit finding from an earlier lab in this series — with no funded training plan item connecting the two until this assessment. I also found a required certification that had quietly expired, held by the team's most senior incident responder.

Neither of those is hypothetical. That's what happens when "we know we have a gap" never gets tied to "here's the money and the date to close it."

Full code, case study, blank training &amp; certification policy template, and a completed assessment report are on GitHub — link in comments.

#CyberSecurity #GRC #SecurityTraining #Certifications #SAMA #NCA #InfoSec #SaudiArabia #WorkforceDevelopment

---
NOTES FOR POSTING (delete before publishing):
- Best visual: screenshot the Skills Matrix page — the dot-based level visualization with the red "gap 2" label makes the point instantly, more than a table of numbers would.
- A second image of the Certifications page showing the red "Expired" pill next to an amber "Expiring Soon" pill works well as supporting proof.
- GitHub link goes in the first comment, not the post body.
