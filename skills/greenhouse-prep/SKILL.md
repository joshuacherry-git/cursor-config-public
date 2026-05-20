---
name: greenhouse-prep
description: >-
  Produce structured Greenhouse interview feedback from raw interview notes.
  Extracts strengths, opportunities, question asked, value-fit ratings, and an
  overall hiring recommendation. Use when the user says "greenhouse prep",
  "interview feedback", "scorecard", "greenhouse scorecard", "write up interview",
  "interview notes", or asks to format notes for Greenhouse.
---

# Greenhouse Interview Feedback

Transform raw interview notes into a structured Greenhouse scorecard.

## Workflow

1. If the **role** and **level** are not apparent from the notes or conversation context, ask before drafting.
2. **Assume this interview is part of a full onsite loop** — not a first-round technical screen — unless the user explicitly says otherwise. Scope strengths, opportunities, and the recommendation to the specific dimensions this round was responsible for evaluating. Do not speculate about how the rest of the loop should cover gaps, and do not add "future rounds should probe X" style commentary. Focus only on what the user evaluated and the conclusions they drew.
3. If the notes lack sufficient signal for any section, ask briefly.
4. Produce the scorecard using the template below.
5. **Voice-match the output**: after drafting the scorecard, invoke the `voice-match` skill (operation `apply`, medium `doc-body`) to rewrite each prose section (Strengths, Opportunities, "What question did you ask?", the excitement paragraph, Key Take-Aways, and the recommendation rationale) in the user's voice. Preserve the section structure, the "TC"/"they" convention, ratings, and any concrete evidence verbatim. Skip voice-matching for the table cells (terse evidence fragments) unless they are full sentences. If the `voice-match` skill is unavailable, note that briefly to the user and return the draft as-is.

## Voice

Write all output in **first person** ("I asked...", "I noticed...", "I'd recommend..."). Refer to the candidate as **"TC"** (the candidate) or **"they/them"**. Never use the candidate's name. Never use gendered pronouns (he/him, she/her).

## Output Template

### Strengths

- First-person, evidence-backed bullet points. ("I was impressed when they...")

### Opportunities

- First-person observations of gaps or concerns. ("I didn't see evidence of...", "They struggled with...")

### What question did you ask?

State the question in first person. ("I asked them to...")

### If you are submitting a Yes or Strong Yes rating below: Why are you excited to have this person on the team and/or working at Reddit?

2-4 sentences in first person. If the recommendation is No or Definitely Not, write: *"N/A — see Key Take-Aways."*

### Value-Fit Ratings (1-5)

Only rate dimensions with sufficient signal. Otherwise write "Insufficient signal."

| Value | Rating | Evidence |
|-------|--------|----------|
| **A Winner** — proactive, ambitious, gets results | | |
| **Problem Solver** — defines problems, finds opportunities, moves efficiently | | |
| **Reliable** — does what they say they will | | |
| **Smart** — shows good judgment and learns quickly | | |
| **Team Player** — collaborative, selfless, helps others succeed | | |

### Key Take-Aways

First-person conclusions, pros, and cons drawn from what *you* observed in *this* round. Do not list things "other rounds should probe" or recommend follow-up coverage for the rest of the loop — the hiring manager owns loop composition. Follow-ups are appropriate only when they're things *you* would do (e.g. "I'd want to re-check this in a working session if we move forward").

### Overall Recommendation

**Definitely Not** | **No** | **Yes** | **Strong Yes** — one-sentence rationale in first person.

## Guidelines

- **Default posture is skeptical.** The bar is high. A "Yes" means you'd stake your reputation on this hire. A "Strong Yes" means you'd fight to close them. Absent clear, strong evidence, lean toward No.
- **Stay in your lane.** This is one round in a full onsite loop. Evaluate and conclude only on what *you* probed. Do not write "the system design round should cover X" or "future rounds need to assess Y" — that's the hiring manager's job, not the interviewer's.
- **Strengths must clear the bar for the level.** "Solid" or "adequate" answers are not strengths — they're table stakes. Only highlight things that genuinely stood out.
- **Don't soften Opportunities.** If something was weak, say so plainly. Euphemistic framing ("could grow into...") obscures signal for the hiring manager.
- **Silence is signal.** If the candidate didn't demonstrate a value in the dimensions you were evaluating, note it — don't gloss over. But don't penalize them for dimensions outside this round's scope.
- Calibrate ratings to role and level — what's strong for an L4 may be expected for an L6.
- Evidence over impression. Match the rating to the narrative.
- Do not fabricate value-fit ratings without signal.
