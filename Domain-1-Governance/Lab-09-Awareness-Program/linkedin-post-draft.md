# LinkedIn Post Draft — Lab 09

---

**Main version**

In July 2020, attackers didn't hack Twitter's systems with some exotic exploit. They called employees on the phone, pretended to be IT support, and asked for access. It worked. Dozens of high-profile verified accounts — political figures, celebrities, major companies — got hijacked to push a crypto scam, and Twitter had to freeze every verified account from tweeting while it figured out how bad the damage was.

Most security awareness programs, even today, are built almost entirely around email phishing. Vishing — phone-based social engineering — barely gets tested, even though it's exactly what took down Twitter.

For Lab 09 of my Saudi Cybersecurity Compliance Labs series, I built the tracker that treats the phone as seriously as the inbox.

**Security Awareness & Training Program Tracker** (Flask + SQLite, Dockerized, same clean UI as the rest of the series):

→ An **Employee Roster** with a privileged-access flag — because the Twitter attackers specifically targeted people with access to sensitive internal tools
→ A **role-based Training Catalog** including a dedicated Vishing & Social Engineering Awareness course, not just generic "cybersecurity 101"
→ **Simulation Campaigns across multiple channels** — email phishing AND vishing — with per-employee outcomes tracked
→ Automatic **repeat-offender flagging**, and a specific alert for privileged employees who fail a vishing simulation — the exact risk profile behind the Twitter breach

I seeded it with a realistic dataset and ran the Twitter pattern directly: a privileged IT support employee provided credentials during a simulated vishing call impersonating — you guessed it — IT support. The dashboard flags it instantly as a Critical risk, distinct from a routine email phishing miss.

The most useful thing the data showed, though, wasn't the failure — it was the recovery. One new hire who failed the first email phishing test and clicked a fake credential page went through follow-up training and correctly reported the next simulation. That before/after pair is what a working awareness program actually looks like: not zero failures, but measurable improvement.

Full code, case study, blank awareness policy template, and a completed assessment report are on GitHub — link in comments.

#CyberSecurity #GRC #SecurityAwareness #SocialEngineering #Vishing #SAMA #NCA #InfoSec #SaudiArabia

---
NOTES FOR POSTING (delete before publishing):
- Best visual: screenshot the Dashboard's "privileged employee failed a vishing simulation" alert banner next to the campaign failure-rate bars.
- A second image comparing the new hire's Q1 (failed, clicked) vs Q2 (reported correctly) simulation results tells the improvement story well.
- GitHub link goes in the first comment, not the post body.
