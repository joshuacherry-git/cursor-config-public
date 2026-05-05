# Harvest plan

Detailed workflow for the stratified corpus harvest used by `bootstrap` and (with a smaller delta) `refresh`. The skill's `SKILL.md` references this file for execution.

## Anti-recency-bias and consistency principles

Every harvester applies these so the resulting voice profile reflects the user across contexts, not just last month's projects.

- **Time stratification** — divide the lookback window (default 24 months) into monthly buckets; sample evenly from each bucket. Older months get the same per-bucket target as recent ones.
- **Audience stratification** — per source, enumerate the top distinct audiences (Slack channels and DM partners, doc collaborators, email recipients, meeting types) and cap per audience to prevent any one channel/relationship dominating.
- **Topic stratification** — after initial harvest, cluster by topic (lightweight keyword/embedding clustering during distillation) and downsample over-represented clusters.
- **Length stratification** — sample across length buckets (very short / short / medium / long) so the profile captures both one-liners and paragraphs.
- **Role stratification** — explicitly seek samples where the user is: author/initiator, reviewer/responder, decision-maker, questioner, teacher, learner.
- **Register stratification** — explicitly cover casual chat, professional sync, formal long-form, presentation-style.
- **Quote/paste filtering** — exclude content clearly quoting others, pasted code blocks, and boilerplate so we capture original voice only.
- **Hold-out split** — reserve ~10% per source to `corpus/holdout/` for blind validation in Pass D of distillation. Stratify the hold-out so it covers the same time/audience distribution as the main corpus.

## Output schema (all sources)

Each row in `corpus/<source>.jsonl` is one snippet:

```json
{
  "id": "<source>-<sha1-prefix>",
  "source": "slack | docs | doc-comments | meetings | email | cursor",
  "text": "the actual user-authored text",
  "ts": "2025-08-14T14:33:00Z",
  "stratum": {
    "month": "2025-08",
    "audience": "channel-name | recipient-domain | meeting-type | session-id",
    "length_bucket": "xs | s | m | l",
    "role": "initiator | responder | reviewer | questioner | teacher | learner | unknown"
  },
  "meta": {
    "channel_id": "...",       // source-specific extras
    "doc_url": "...",
    "thread_ts": "...",
    "meeting_id": "..."
  }
}
```

`scripts/corpus_stats.py` reads this schema; keep it stable.

## Identity auto-verification

Before any source-specific harvest, optionally call:

- `slack_read_user_profile` with no arguments → returns the current Slack user (handle, email, display name). Compare against `identity.yml` and warn on mismatch.
- For Google Workspace identity (`full_name`, `display_name`), no tool currently exposes a "whoami" endpoint. Trust the values in `identity.yml`.
- Gmail and Glean Drive harvesters use implicit auth (`from:me`, `owner:me`); the explicit values in `identity.yml` are still needed for the `meeting_lookup` `participants` filter and for filtering doc comments to your authored entries.

## Per-source workflows

### Slack (~1500-2500 messages)

Tool: `slack_search_public_and_private`. Limit is 20 results per call; pagination via `cursor`.

**Discovery pass** — for each month bucket in the lookback:

1. Call `slack_search_public_and_private` with `query: "from:<@U05L5J9UEMB>"` and date filters `after:YYYY-MM-DD before:YYYY-MM-DD` for the month. Use `limit: 20`.
2. Page using the returned `cursor` until exhausted or 200 results retrieved for the month (whichever first).
3. Track per-channel counts encountered.

**Stratified sample** — after discovery:

- Compute target per (month × channel) cell so the total lands in 1500-2500.
- Cap each cell so any single channel can't dominate (e.g., max 30 per channel per month).
- Reserve a separate quota for DMs (`channel_types: "im"`) so casual 1:1 voice is represented.
- Include both top-level posts and threaded replies. Use a follow-up search with `is:thread` to ensure thread coverage.

**Filters**:

- Exclude bot messages (`include_bots: false`, default).
- Exclude messages whose text is mostly a code block, link, or quoted content (heuristic: <30% non-code/non-link characters).
- Exclude one-word messages (":thumbsup:", "yep") unless the "xs" length stratum is explicitly being filled.

**Length buckets**: xs (<20 chars), s (20-100), m (100-400), l (400+).

### Google Docs body (~30-50 docs)

Tools: `search` (Glean) for discovery, then `read_document` for body retrieval.

**Discovery** — per month bucket:

1. `search` with `query: "*"`, `owner: "me"`, `app: "gdrive"`, `before` and `after` set to the month, `num_results: 50`. Paginate via `cursor` if more.
2. Filter results to Google Docs (skip Sheets, Slides, Folders unless explicitly desired).

**Sampling**:

- Stratify by month and by doc type heuristic from the title/path: spec / retro / RFC / design / status / 1:1 / personal-notes / other.
- Cap per type per month so no doc type dominates.
- Include `seeds.signature_doc_urls` from `identity.yml` regardless of stratification.

**Body extraction** — per selected doc:

1. `read_document` with the URL.
2. For long docs (>5k chars), sample sections: intro paragraph, conclusion paragraph, plus 1-2 mid-document paragraphs chosen for argumentative density (look for "I think", "the key point", "we should").
3. Strip headings, bullets, code blocks, and inline citations from the captured text — we want prose voice, not formatting.

**Length buckets**: s (<500 chars sampled), m (500-2000), l (2000+).

### Google Doc comments (~300-500 comments across 30+ docs)

Tool: `analyze_doc_comments` per Google Doc URL.

**Doc URL pool** — assemble from two sources:

1. Docs the user authored (already enumerated for the docs body harvest).
2. Docs the user commented on but did not author. Enumerate via `search` with `from: "me"`, `app: "gdrive"`, monthly buckets across the lookback.

**Sampling**:

- Stratify by month and by doc-owner relationship: own-doc / teammate-doc / cross-team-doc / exec-doc.
- Cap per relationship per month.

**Per doc**:

1. Call `analyze_doc_comments` with the URL.
2. Filter to comments authored by the user (match by name from `identity.yml`).
3. Capture both top-level comments and replies. Replies show reactive tone, which is gold.
4. Skip comments that are pure resolutions ("Done", "Fixed") unless filling the xs stratum.

**Length buckets**: xs (<30), s (30-150), m (150+).

### Meeting transcripts (~30-50 meetings, user's spoken segments only)

Primary tool: `meeting_lookup` with `extract_transcript: true`.

**Discovery** — per month bucket:

1. Call `meeting_lookup` with `participants: ["<full_name>"]`, `after`/`before` set to the month, `extract_transcript: false` (just enumerate).
2. Inspect titles and participant lists to classify meeting type: 1:1 / team-standup / project-sync / cross-functional / interview / customer-call / all-hands.
3. Audience composition: peer-only / mixed-seniority / external.

**Sampling**:

- Stratify by meeting type and audience composition across months.
- Include `seeds.core_meeting_types` from `identity.yml` regardless.
- Cap per (type × month) cell.

**Per selected meeting**:

1. Re-call `meeting_lookup` with the same filters but `extract_transcript: true` to retrieve transcript.
2. Extract only segments where the speaker label matches the user's name. Concatenate consecutive same-speaker turns into one snippet.
3. Drop transcript artifacts ("[inaudible]", timestamps).
4. Length buckets: xs (<10 words), s (10-50), m (50-200), l (200+).

**Zoom coverage**:

- `meeting_lookup` returns Google Meet recordings reliably. Zoom Cloud Recordings appear only if the org has Zoom→Glean integration enabled.
- **Fallback 1**: `search` with `app: "gong"`, monthly buckets, `from: "me"` — Gong commonly indexes Zoom calls in sales/customer-facing contexts. Use `read_document` on results to extract transcripts.
- **Fallback 2**: `search` with `app: "gdrive"`, `query: "transcript"`, monthly buckets, `from: "me"` — picks up Zoom auto-uploaded transcript files in Drive.
- Document Zoom hit/miss counts in `corpus/MANIFEST.md` so the user knows the coverage shape.

### Gmail outbound (~200-300 emails)

Tool: `gmail_search`.

**Discovery + sampling** — per month bucket:

1. Call `gmail_search` with `query: "from:me label:SENT after:YYYY-MM-DD before:YYYY-MM-DD"`. Inspect recipient(s) and length.
2. Stratify by recipient type:
   - **internal-individual** — single internal recipient
   - **internal-group** — multiple internal recipients or a list/group address
   - **cross-functional** — recipients in clearly different functions/orgs
   - **external** — non-corporate domains, customers, vendors
3. Cap per (recipient-type × month) cell.

**Filters**:

- Exclude one-line acknowledgements ("Thanks!", "Sounds good") unless filling xs stratum.
- Exclude forwards (subject starts with "Fwd:") — voice in forwards is mostly the original sender's.
- Strip email signature, quoted prior messages, and disclaimers from captured text.

**Length buckets**: s (<200), m (200-800), l (800+).

### Cursor agent prompts (~500+ user turns)

Local script: `python scripts/extract_cursor_turns.py`.

The script walks `~/.cursor/projects/Users-joshua-cherry-code/agent-transcripts/<uuid>/<uuid>.jsonl`, extracts user turns, dedupes near-duplicates, and writes stratified output to `corpus/cursor-agents.jsonl`.

**Stratification** (handled in the script):

- By session date (file mtime → month bucket).
- By session length (turns per session): short one-shot / iterative / extended.
- By turn position within session: opener / mid-session / closer.

**Filters** (in the script):

- Skip turns whose content is purely tool output / system reminder / external link block. The script extracts only the inner `<user_query>...</user_query>` content where present.
- Skip empty turns and one-word turns ("yes", "go").
- Dedupe via shingled-hash near-duplicate detection.

## Manifest format

After harvest, write `corpus/MANIFEST.md` with:

```markdown
# Corpus manifest

Generated: YYYY-MM-DD HH:MM

## Per-source counts

| Source | Snippets | Hold-out | Time range | Notes |
|---|---|---|---|---|
| slack | 1842 | 184 | 2024-05 .. 2026-04 | DMs: 312 |
| docs | 38 | 4 | 2024-05 .. 2026-04 | |
| doc-comments | 421 | 42 | 2024-05 .. 2026-04 | |
| meetings | 36 | 4 | 2024-08 .. 2026-04 | Zoom hits: 8 / 36 (Gong fallback used) |
| email | 247 | 25 | 2024-05 .. 2026-04 | |
| cursor | 612 | 61 | 2024-09 .. 2026-04 | |

## Stratum coverage

- Time bucket coverage: NN / 24 monthly buckets non-empty per source.
- Audience coverage: top N audiences per source captured.
- Length bucket distribution per source.

## Coverage gaps

- e.g. "Zoom: org has no Glean integration; only N transcripts via Gong fallback."
- e.g. "Pre-2024-09 Cursor agent transcripts unavailable (skill installed later)."

## Dedupe stats

- Near-duplicate rejections per source.
```

## Refresh delta

`refresh` uses the same workflow but with `lookback_months: 3` (or whatever the user specifies). It appends to existing JSONL files and dedupes against existing rows by `id` field.
