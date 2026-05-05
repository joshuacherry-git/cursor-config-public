# Mode overlay: spoken

Loaded with `voice_profile.md` when `medium: spoken` (script cleanup, transcript polish).

## Medium description

**Google Meet transcripts** segmented into snippets (**small corpus N ~11 meets—coverage caveat**): oral **discourse-marker stacks** (**like / uh / um / you know / i mean**) + sense-test / econ-method vocabulary. **`filler_density_per_1k` ~94.2** overall (`stats/meetings.json` overlay section); **ranges by forum**: **project-sync ~63**, **team-standup ~95**, **1on1 ~104** (**mini-profile strata**).

## Fragment-faithful default

Real spoken transcripts—especially **1:1** and **project-sync**—are **fragmentary and disfluent:** half-clauses, false starts, fillers (`uh`, `so like`, `i guess`), trailing `…`.

**Default cleanup** preserves that grain: keep **some** fillers, allow incomplete sentences, **avoid** layering signpost-heavy polish not present in the source.

The **polished** lane—importing methodology lexicon (“Assume… inject… compare…”)—applies **only** when the caller clearly signals **scripted/exec** transcript cleanup or rehearsed-talk polish. Otherwise treat executive-method narration as **opt-in**.

## Deltas from core voice

Never import wholesale into slick written prose:

- **Allow light spoken residue** (“like”, “yeah”, sporadic truncated clause) proportional to fidelity ask—**thin for executive-facing scripts**, heavier for authenticity-only cleanup.
- **Hedge climb vs sync:** **`1on1` hedges peak ~17.7/1k**, **`project-sync` ~9.7/1k**—tighten fillers when rewriting **mixed-room product sync**.
- **`you`-weighted dyadic** cadence plausible in conversational coaching excerpts—clip for mixed audiences.
- **Question marks (~5.0/1k overall)** spike in **tiny `xs`** utterance buckets—preserve ping questions (`…sensible?`) without rewriting every filler out.
- **Punctuation scarcity** in transcripts (written `—`/parens essentially **zero** pooled)—don't “legalize” into memo typography unless instructed.

## Length norms (`stats/meetings.json`)

- Overall sentence stats: mean ~**10.7**, **p50 ~7**, **p90 ~25** words.
- **Paragraph** median ~**11w**, longer turns in relational forums.

## Opener patterns (anonymized)

1. **`Yeah … No … I could totally agree`** (**affiliation stack**).

2. **`would you mind … high-level overview`** (**polite ask**).

3. **`Assume for now [model behaves] … what would you tighten next?`**

4. **`Inject a shock … comparative statics … plausible responses`** (**method narration**).

5. **`sorry, go ahead`** floor yielding.

## Forbidden in this mode

- Strip **all** disfluency (**robotic**) OR add MLM-ish signposting **not** in transcript.
- Do **not** import **method-narration** vocabulary (**`comparative statics`**, **`sense test`**, **`sequencing alternatives`**) into a naturally fragmentary transcript **unless** the caller explicitly asks for scripted/exec polish matching that lane.
- **Polish away every filler** — strip roughly **half** of `um`/`uh` noise only; preserve **`so`**, **`like`**, **`i guess`**, **`i mean`** as authentic oral markers unless source is explicitly scripted-tight.
- **Import oral filler ladders** back into **`doc-body`/`slack`** rewrites (**cross-contamination barred**).

## Exemplars

1. *“Assume the draft model holds—given that—where next?”*

2. *“inject a perturbation… read out which directions look economically plausible…”*

3. *“Yeah… completely aligned we shouldn’t distract the room with tooling theater.”*

4. *“Worried casual users infer more precision than the panel actually encodes…”*

5. *“Trust the methodology—we’re asking experts to reconcile quantitative story with rollout reality.”*

6. *“It’s gnarly on calendar—prefer minimizing workshop prep tax on IC time.”*

