---
name: voice-match
description: Rewrites a draft (LLM output, email reply, doc paragraph, Slack message, PR comment, agent prompt) into the user's personal voice using a distilled voice profile grounded in their own Slack messages, Google Docs, doc comments, meeting transcripts, sent email, and Cursor agent prompts. Also produces a one-shot speaking style and clarity report from meeting transcripts. Use when the user says "voice this", "in my voice", "match my voice", "humanize this draft", "make this sound like me", "ghostwrite", "voice-match", or asks to analyze their own speaking style or communication clarity from meeting transcripts.
disable-model-invocation: true
---

# voice-match

Rewrite a draft in the user's voice, grounded in a real corpus they control.

This skill has four operations. The default is `apply` (rewrite a draft). The other three (`bootstrap`, `refresh`, `analyze-speaking`) build or refresh the underlying voice profile and produce a separate speaking style report.

## Files in this skill

- `voice_profile.md` — core voice rules, exemplars, smell tests. Loaded on every `apply` call.
- `modes/<medium>.md` — small overlays for: `slack`, `doc-body`, `doc-comment`, `spoken`, `pr-review`, `agent-prompt`, `email`. Loaded on `apply` when the caller specifies a medium.
- `harvest-plan.md` — detailed stratified harvest workflow with per-source MCP call patterns, volume targets, and dedupe rules. Read during `bootstrap` and `refresh`.
- `identity.yml` — Slack user_id, full name, email(s) used by harvesters. Confirm before running `bootstrap`.
- `corpus/` — raw harvested snippets (gitignored). Reference for `bootstrap`/`refresh`/`analyze-speaking`. NEVER load into context during `apply`.
- `scripts/extract_cursor_turns.py` — local extractor for Cursor agent transcripts.
- `scripts/corpus_stats.py` — stylometric baselines per source/stratum.

---

## Operation: apply (default)

**Inputs**: a draft (the text to rewrite) + optional `medium` hint (`slack` | `doc-body` | `doc-comment` | `spoken` | `pr-review` | `agent-prompt` | `email` | `general`). Default medium is `general`.

**Steps**:

1. Read [voice_profile.md](voice_profile.md). If a medium other than `general` is specified, also read `modes/<medium>.md`. Do NOT load anything from `corpus/`.
2. Identify what the draft is *saying* — preserve meaning, structure, claims, and any concrete facts/numbers.
3. Rewrite using the rules in `voice_profile.md` and the overlay in the medium file. Bias toward the favored constructions and against the banned ones.
4. Run the smell tests defined at the bottom of `voice_profile.md` against the rewrite. If any fail, revise once and re-check.
5. Return only the rewritten text. Do not add commentary, framing, "Here's a rewrite:", or notes unless the caller explicitly asked for a diff or rationale.

**Common smell tests** (final list lives in `voice_profile.md`, refined by distillation):

- No LLM filler: "It's worth noting", "Let's dive in", "It's important to note", "In conclusion", "I hope this helps", "Feel free to".
- Em-dash use within the user's baseline range (not the LLM-default heavy use).
- Sentence length distribution within baseline range (no monotone medium-length sentences).
- No unnecessary hedging that the user wouldn't add.
- Opener pattern matches the medium (e.g. Slack often skips greetings).

---

## Operation: refresh

Re-harvest a delta window and re-distill. Use when the underlying voice may have shifted (new role, new project type, etc.) or quarterly.

**Steps**:

1. Read `identity.yml` and confirm with the user that values are still correct.
2. Read [harvest-plan.md](harvest-plan.md) and run the harvest workflow with `lookback_months: 3` (or whatever delta the user requests). Append new snippets to existing `corpus/*.jsonl` files; dedupe against existing rows.
3. Run `python scripts/corpus_stats.py` to refresh stylometric baselines in `corpus/stats/`.
4. Run the multi-pass distillation (see "Distillation" section below) using the full corpus.
5. Show the user a diff of `voice_profile.md` and each `modes/*.md` versus the previous version.
6. Pause for redaction review before saving. Save only after user approval.

---

## Operation: bootstrap

First-time setup. Thorough, slow, runs the full stratified harvest across the 24-month lookback. Plan for a long session — the agent will make hundreds of MCP calls.

**Steps**:

1. **Confirm identity**: Read `identity.yml`. Auto-verify Slack identity by calling `slack_read_user_profile` (no args defaults to current user); compare against the file and warn on mismatch. Google Workspace `full_name` and `display_name` are not programmatically fetchable from current tools — ask the user to fill any blank fields. Do not proceed until at least `slack.user_id`, `google.full_name`, and `google.primary_email` are populated.
2. **Run the stratified harvest**: Read [harvest-plan.md](harvest-plan.md) and execute every per-source workflow there. Each source produces a JSONL file in `corpus/`. Track progress per stratum.
3. **Compute baselines**: Run `python scripts/corpus_stats.py` to produce `corpus/stats/<source>.json` with stylometric metrics per source and per stratum.
4. **Split hold-out**: Reserve ~10% of each source's snippets to `corpus/holdout/<source>.jsonl` (random sample, but stratified — keep the same time/audience distribution). The distillation must NOT see the hold-out.
5. **Write `corpus/MANIFEST.md`**: Record per-source counts, time range covered, audience distribution, dedupe stats, hold-out splits, and any coverage gaps (especially for Zoom).
6. **Run multi-pass distillation** (see below).
7. **Pause for redaction review**: walk the user through `voice_profile.md` and each `modes/*.md`. Anonymize any names, project codenames, customers, or confidential references in exemplars before saving.
8. **Optional**: continue to the `analyze-speaking` operation while transcript data is fresh.

### Multi-pass distillation

Use the `swarm-orchestrator` skill if available for parallelism. Otherwise run sequentially.

**Pass A — per-source extractors** (one subagent per source). Each receives one source's corpus + its stylometric stats and produces a per-source mini-profile to `corpus/.distill/<source>.mini.md`. Capture: lexical fingerprints, sentence rhythm, opener/closer patterns, formatting habits, register cues, ~10 representative exemplars per source.

**Pass B — cross-stratum consistency check** (single subagent). Reads all mini-profiles + per-stratum stats. Classifies every observed pattern as one of:
- **Stable** — present across most strata → goes into core voice.
- **Medium-specific** — strong in one source/medium only → goes into the matching `modes/*.md`.
- **Drift** — present only in recent buckets → flag and downweight as potential recency artifact.
- **Contradiction** — sources disagree → flag for human review.

Output: `corpus/.distill/cross-stratum.md`.

**Pass C — synthesizer** (single subagent). Produces final `voice_profile.md` (stable patterns + ~30-40 universal exemplars + smell tests) and each `modes/*.md` (overlay + ~5-10 medium exemplars). The synthesizer is instructed to:
- Prefer stylistically rich snippets over content-rich ones.
- Anonymize names, project codenames, customers in exemplars.
- Keep `voice_profile.md` under ~300 lines.
- Keep each `modes/*.md` under ~100 lines.

**Pass D — adversarial reviewer vs hold-out** (single subagent). Reads the produced profile + a curated set of "neutral seed" passages, rewrites them in voice using only the profile, then compares against the held-out exemplars. Flags:
- Tone mismatches (formality, hedging level).
- Patterns the hold-out shows but the profile misses.
- Profile rules that don't appear in the hold-out (over-rules).

If issues are found, loop back to Pass C with the reviewer's notes. Cap at 3 rounds, then surface remaining issues to the user.

---

## Operation: analyze-speaking

Side task. Bundled with this skill because the meeting transcripts are already harvested. Output is a markdown report in the user's journal, not a runtime resource.

**Inputs**: `corpus/meetings.jsonl` (your spoken segments, already stratified by meeting type / audience / month).

**Output**: `~/code/thoughts/projects/speaking-analysis-YYYY-MM.md` (date-stamped so trend tracking works).

**Steps**:

1. If `corpus/meetings.jsonl` is missing or empty, suggest running `bootstrap` first (or just the meeting harvest section of `harvest-plan.md`).
2. Run `python scripts/corpus_stats.py --source meetings --spoken-features` to compute spoken-specific metrics (filler density, false-start rate, abandoned-sentence rate) on top of the standard baselines.
3. Read the stats and a stratified sample of transcript segments. Produce the report with these sections, in this order:
   1. **Corpus summary** — meetings, total minutes, breakdown by meeting type / audience / time, coverage caveats (especially Zoom).
   2. **Verbal patterns** — filler frequencies (um, uh, like, you know, right, so), false-starts, abandoned sentences, hedge density.
   3. **Clarity metrics** — avg spoken sentence length, sentence completion rate, jargon density (with examples), signposting frequency, definition-providing rate when introducing terms.
   4. **Pacing & turn-taking** — avg turn length, longest turns, distribution of short reactions vs sustained explanations, conversation share by meeting type.
   5. **Question vs declaration** — ratio, breakdown of question types, where the user tends to ask vs tell.
   6. **Audience adaptation** — how patterns shift across 1:1 vs group, peer vs senior vs report, internal vs external.
   7. **Conviction & hedging** — confident vs hedged statements, hedging clusters, recovery patterns after disagreement.
   8. **Topic transitions** — abrupt vs bridged, signposting use at transitions.
   9. **Comparison over time** — has any of the above shifted across the lookback window?
   10. **Top 5 recommendations** — concrete, ranked, each with 1-2 anonymized example quotes from the user's own transcripts and a suggested rewrite.
4. Anonymize all example quotes (replace participant names, projects, customers with generic placeholders) before writing.
5. **Critical/honest framing** — no sycophancy. Surface real weaknesses. The recommendations section is the most important output; treat it like a `critical-review` skill invocation.
6. Save to `~/code/thoughts/projects/speaking-analysis-YYYY-MM.md` and tell the user where it is.

---

## Trigger phrases (for the description's "use when" clause)

- "voice this" / "voice-match this" / "in my voice" / "match my voice"
- "make this sound like me" / "humanize this draft" / "ghostwrite"
- "rewrite in my voice" / "rewrite as me"
- For the side task: "analyze my speaking" / "speaking style report" / "communication clarity" / "how clearly do I speak"

---

## Privacy reminders

- `corpus/` is gitignored. Raw Slack/doc/email/meeting content stays local.
- Profiles and mode files commit to git via the `sync-config` skill, but only AFTER the user has reviewed and redacted exemplars.
- The speaking analysis report is written to `~/code/thoughts/projects/`, which has its own privacy posture; quotes there are anonymized.
- Never load corpus content into the agent context during `apply` — only the distilled profile + overlay.
