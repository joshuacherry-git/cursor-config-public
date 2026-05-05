# Mode overlay: Slack

Loaded with `voice_profile.md` when `medium: slack`.

## Medium description

Asynchronous Slack: **DM-skew corpus** (**~91% `im`** in harvest; **narrow Mar–Apr 2026** window—**confidence: medium-low** generalizing beyond engineer-DM “lab memo” genre.) Treat “Round” briefing voice as authentic for **long technical memos**, not assumed for every future channel/quip culture.

## Bimodal corpus warning

Two registers show up strongly in corpus—**do not blend** them; **match the input draft’s shape:**

1. **Memo register:** Long forensic notes with **`Round [N]`** scaffolding, **`Devil`/`Champion`** lines, pasted tables/logs, dense **`—`** and parentheses, full sentences.
2. **Brainstorm-DM register:** Ultra-casual lowercase threads, sideways hedges, often ending in **`wdyt`**, **`i guess`**, **`i think`**—not mini-charters.

**Brainstorm-DM recipe when the source looks like that:** lowercase; omit terminal periods on standalone one-liners when that matches source; hedge openers (`btw`, `i guess`, `kinda thinking`, `random idea:`); favor questions; close with **`wdyt?`** or trail off.

**Memo recipe** when the source is long-form status/forensics: numbered headers; fenced tables/logs OK; richer dash/parenthesis typography.

Choose one register per rewrite; forcing memo scaffolding onto a brainstorm-shaped input is a known failure mode.

## Deltas from core voice

vs **neutral core**:

- **`Round [N] — [Headline]:`** episodic headline + pasted evidence stack (tables, fenced blocks)—**editorial scaffolding** climbs sharply.
- **Typography:** Elevated **`—`** (~**11.84**/1k), **`;`** (**~3.78**/1k), **`(`** (**~29.8**/1k `paren_open`—`stats/slack.json`).
- **`Devil/Champion` dialectic** permissible **but downweighted globally** (**single rapport / spike month amplification**—use sparingly unless user signals that memo voice).
- **Hedge scarcity in long posts** (**~1.22** hedges/1k overall) vs hedge clusters in casual short DMs (**might / I think**).
- **`llm_filler_density` ~0** in stats slice—maintain terse operational backbone.
- **Emoji:** Sparse overall; `:white_check_mark:`-style **functional checklist** cues when icons appear—not reaction-stack tone by default (**public-channel emoji culture unseen**).

## Length norms (`stats/slack.json` `by_length_bucket`)

Weighted by **memo paste** morphology:

| bucket | snippets | aggregate words ≈ |
|---|---:|---:|
| `l` (long) | 65 | **~36,926** (dominant paste mass—**median para p50 ~485w** inside long rows) |
| `m` | 10 | ~495 |
| `s` | 11 | ~161 |

Interpretation: “typical Slack **row** averages **~427w** corpus-wide (**37,588/88**) because **few huge memos dominate** short pings.

## Opener patterns (anonymized)

1. **`Round [N] — …:`** serialized brief headline.
2. **`[Topic]-Track Debate — Round …`** multi-round arc label.
3. **`[Project] follow-ups — progress update`**
4. **`i think …` / `so yea …` / `ok but …`** (casual **DM** substrate).
5. **`Well done` / `Glad to see this`** compressed affirmation.
6. **`@`-style mention to **[Person]** for access/permissions** (**channel slice small**).

## Forbidden in this mode

- **Retrofitting public-thread interrupt grammar** absent evidence (corpus MCP-limited).
- **Forcing Devil/Champion** into every substantive post (**overlay-only / rapport-tied spike**—downweight).
- **Emoji ceremony** stacks as tone carrier when checklist semantics aren’t needed.
- **`Hi team`** windups before headline payload in memo genre (**greetings deliberately thin**).
- Do **not** impose memo scaffolding (`Round`, fenced tables, Devil/Champion framing) on a brainstorm-DM-shaped input.
- Do **not** add greetings to either register (**openers stay thin—no `Hi`** unless present in source and medium overlay says otherwise).

## Exemplars

1. **`Round [N] — [Result headline]:`** table block → numbered next steps (**teaches headline + instrumentation**).

2. **Champion/Devil excerpt** debating tail risk vs uplift with metrics (**teaches optional dialectic**).

3. **`What I want next` numbered list → `What do you want me to prioritize?`** (**delegation closer**).

4. **`there is a parallel workstream on [topic]; btw`** sideways org map (**lowercase aside**).

5. **`Ye… just needed a runnable slice—not the full vendor stack debate`** (**narrow negation DM**).

6. **`Root cause ([forensic label]):`** bullets **`Proposed fixes (one of):`** numbered menu (**forensic memo**).

7. **`Status`** RUNNING / QUEUED bullets + **`Shipped this round`** artifact line (**checkpoint layout**).

8. **`there is a separate workstream … btw`** sideways map (**FYI comma**).

