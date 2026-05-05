# Corpus manifest

Generated: 2026-05-04 during initial bootstrap.

## Per-source counts

| Source | Main | Holdout | Time range covered | Notes |
|---|---:|---:|---|---|
| slack | 88 | 8 | 2026-03 .. 2026-04 (2/24 buckets) | MCP-limited, mostly DMs |
| docs | 57 | 5 | 2024-05 .. 2026-04 (10/24 buckets) | Cleaned of Notes-by-Gemini contamination |
| doc-comments | 95 | 8 | 2024-05 .. 2026-04 (13/24 buckets) | |
| meetings | 793 | 87 | 2025-11 .. 2026-04 (5/24 buckets) | Google Meet only; no Zoom indexed |
| email-sent | 79 | 5 | 2024-10 .. 2026-04 (17/24 buckets) | Gmail dedupes overlapping threads aggressively |
| cursor-agents | 503 | 45 | 2026-04 .. 2026-05 (2 buckets) | mtime-bucketed; transcript files re-touched recently |

**Total**: 1615 main + 158 holdout = 1773 snippets across 6 sources.

## Stratum coverage summary

- **Time depth**: doc-comments and docs reach back to 2024-05 (full lookback). email reaches to 2024-10. meetings, slack, cursor are recent-only due to indexing/MCP limits.
- **Audience diversity**: Slack ~91% DMs (channel search MCP unstable); meetings span 1on1/team-standup/project-sync; emails span internal-individual/internal-group/external; docs span design/spec/retro/status/other.
- **Length distribution**: Strong representation across xs/s/m for most sources. `l` bucket sparse for docs and meetings (most authored prose snippets are <2000 chars; spoken turns tend to be <200 words).

## Coverage gaps (significant)

- **Slack**: `slack_search_public_and_private` MCP returned empty for date-windowed `from:` queries and rate-limited on broad pagination. Only ~96 messages captured vs 1500-2500 target. Time depth is 2 months. This is an MCP-side limitation, not a workflow issue.
- **Meetings/Zoom**: No Zoom transcripts available — the org has no Glean Zoom integration, no Gong indexing for this user, and only one Drive Zoom-style transcript surfaced (not merged). All 11 captured meetings are Google Meet. 2024 and most of 2025 have no indexed transcripts.
- **Docs**: After cleaning out auto-generated meeting note docs, 20 distinct authored docs remain. The user's `owner: me` Drive corpus skews heavily toward Gemini-generated meeting notes vs authored long-form prose.
- **Cursor agents**: Local transcript files were all re-touched in late April 2026 (mtimes), so time bucketing is collapsed. True session-start dates would require parsing JSONL contents.

## Dedupe stats

- Cursor agent extractor: 178 near-duplicates rejected (signature-based), 99 too-short turns skipped.
- Email: ~159 raw outbound items condensed to 84 unique texts after SHA1 dedupe (gmail returns overlapping threads).
- Docs cleanup pass: 138 -> 62 after filtering 44 contaminated titles + 10 contaminated text + 22 no-voice short.
- Slack: dedupe by (channel_id, ts) tuple within harvest, then by row id on append.

## Implications for distillation

- The voice profile will be **strong on**: agent prompts (cursor, 503 snippets), spoken voice in 1on1/team contexts (meetings, 793 snippets).
- **Reasonable on**: doc body (57 snippets but high-signal authored prose), doc comments (95), email (79).
- **Weak on**: Slack mode (88 snippets, mostly DMs, narrow time window) — the Slack mode overlay should be flagged as low-confidence and refined later.
- Time-depth limitations mean the profile may over-index on recent voice. The cross-stratum consistency check (Pass B) should explicitly flag this.

## Refresh recommendations

- Re-run after MCP issues for Slack stabilize.
- Consider Glean `app:slack` filter as alternative Slack discovery path.
- Zoom coverage will improve only if org-side integration is added.
