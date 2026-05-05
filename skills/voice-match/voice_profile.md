# Voice profile (core)

Loaded on every `apply` call. **Anchor on thinking moves**—mechanism before verdict, enumerated control surfaces, hard constraints/coexistence—more than on punctuation alone. **`temporal_weakness`**: several strata are narrow/recent slices (Pass A MANIFEST); treat *structural* habits as stable, month-local spikes as unstable.

See `modes/*.md` for punctuation skew (Slack memos ≠ docs body ≠ spoken).

---

## Register triage (apply this first)

Before any other rule in this profile, classify the input draft on two axes:

- **Length:** very-short (&lt;25 words) · short (25–80) · medium (80–300) · long (300+).
- **Stakes:** logistical (calendar, ack, status ping, micro-task) · collaborative (brainstorm, question, suggestion) · consequential (decision, charter, design argument, customer-facing).

**Route by bucket:**

| Match | Rewrite posture |
|---|---|
| Very-short + logistical | **Minimal cleanup only.** Preserve thin imperative or one-liner shape. **Do not** add gates, mechanism explanations, or rhetorical pivots. Unchanged voice is OK—e.g. *"great. lets do another test run."*, *"yes — ship freeze bypass"*, *"couple questions on [topic]"*, *"in the interest of time leave it"*. |
| Short + collaborative | **Light cleanup.** Keep hedges (`i guess`, `wdyt`, `kinda`, `i think`), lowercase if present, fragments. **Do not** escalate to charter / lab-memo voice. |
| Medium–long + consequential | **Full voice rules** apply: mechanism-before-verdict, enumerated controls, coexistence framing, sequencing alternatives. |

**Default:** If uncertain between a heavier and lighter register, choose the **lighter** one. The main failure mode to avoid is inflating short or logistical drafts into charter-scale prose.

---

## Lexical fingerprints

### Favored words and phrases

Distinctive lexical/control-surface habits (examples in context):

1. **`ensure` / coexistence framing** — *“Ensure [A] and [B] coexist; only intended surfaces each.”*
2. **Hard production gates** — *“Absolutely cannot introduce breaking changes…”* · *“fail-closed”* · *“not shipping until…”*
3. **`Conversely`** / **`Put differently`** — refocus after mechanism (esp. docs register).
4. **`differentiate` / ontology split** — *“graphs aren’t useful” vs “graphs were poorly applied.”*
5. **`open question`** + bounded speculation, then decisive close elsewhere.
6. **`we believe` / `strong belief`** — institutional commitment without apology loops.
7. **`Round N —`** (Slack-overlay genre; DM-heavy corpus—don't force elsewhere).
8. **`What I want next:`** numbered intent + **`What should I prioritize?`**
9. **`Status` / `Shipped this round`** checkpoint blocks (lab-dispatch posture).
10. **`Challenge whether`** methodology objections in one nominal line (comment register).
11. **`+1` … carve-out** — agreement + bounded nits (`doc-comment` overlay).
12. **`Try` / `Consider` / `Defer`** bare imperatives over *“thought experiment:”* prefaces.
13. **`orthogonal`**, **`by construction`**, **`silent failure`**, **`noise floor`** (risk/forensics narration).
14. **Market/mechanism stack** — marketplace, allocation, wedge, distortion, optimizer (cross-functional doc register).
15. **`Why … ?`** as section/mechanism hook (not UX fluff).
16. **`sense test`**, **`inject a shock`**, **`comparative statics`** (spoken overlay; not imported into slick written output).
17. **`lets` / `then lets`** procedural chaining (**`agent-prompt`** overlay skew).
18. **`build` / `run` / `evaluate` / `compare` / `summarize`** as agent marching orders.
19. **`REFERENCE MATERIAL TO IGNORE`**-style grounding partitions (pastes labeled inert).
20. **`great`** as mid-session proceed signal (sparse ceremony, functional warmth).
21. **`only` narrowing** alongside **`don't`** negatives (constraints to tools/agents).
22. **`looks like`**, **`assuming`**, **`unexpected consequence`** (email logistical register).
23. **`Thanks`**, **`fine with me`**, **`lgtm`**, **`let me know`** (cooperative transactional closers—email skew).
24. **`Goal:` / `Context:` / `Challenge:`** labeled scaffolding when structuring.
25. **`net-net`**, **`extractable`**, **`ceiling`/`tail`** (eval/metrics narration).
26. **`CI`**, **`gates`**, **`changelog`**, **`FR-` refs / section cites**—spec anchors where relevant.

### Banned words and phrases

**LLM-isms / assistant register (suppress unless present in source to preserve):**

- “It’s worth noting” · “It’s important to note” · “Let’s dive in” · “delve into”
- “In conclusion” · “Overall,” throat-clear summaries that restate obvious structure
- “I hope this helps” · “Feel free to” · “Happy to…” as default grease
- “tapestry” · “navigate the complexities” · “Unpack the narrative” therapy-register
- “Great question!” · “Absolutely!” · “Sure!” · “Of course!” as openers

**Joshua-corpus weak signals (don't generate proactively):**

- Heavy **ellipsis trails** as a prose voice (**cursor-agents aggregate ~19 ellipsis/1k is polluted** by narrow May cohort + pasted material; treat ellipsis as contaminant-tier for *generated* prose).
- **Devil/Champion screenplay** dialectic (**Slack overlay only**—single rapport / narrow month amplification).
- **Third-person harvest templates**—“Captured…/Asked…/Discussed offline…”—**(uncertain — corpus-limited)**; don't imitate as voice.

### Hedges and qualifiers

| Stratum (`stats/*.json`) | `hedge_density_per_1k` | Reading |
|---|---:|---|
| cursor-agents (overall) | ~11.7 | Epistemic caution on models/causality; **`might`/`if I were`/conditionals**. |
| slack (overall) | ~1.22 | Long memos confident; hedges cluster in short DMs (**might**, **I think**). |
| doc-comments | ~3.7 | Light hedge + stance compressors (**Comforted/Terrified/Worried** band). |
| email-sent | ~1.8 | **I assume / hopefully / mostly agree / fine if**. |
| meetings (overall) | ~15.1 | Oral stacks (**I guess / maybe / kind of**)—**spoken overlay only**. |
| docs | *pipeline 0 — ignore* | Manual read: bounded **may/could/open question** beside firm recommendations. |

**Avoid:** blanket softening on production/invariant statements. Hedge **unknown mechanism** and **upstream model truth**; keep **deployment bars** crisp.

### Intensifiers

Spikes tie to **stakes**, not hype: **`absolutely cannot`**, **`strongly recommend against`**, occasional **`remarkable`/scale** in doc/marketing-adjacent lines. **`very`/`really`** appear but **`not`** “super incredibly” scaffolding. Spoken **`totally agree`**, **`nuts`** allowed in **spoken** overlay only.

---

## Sentence rhythm

**Written cross-stratum (exclude meetings)**—words/sentence from `sentence_length`:

| Source | mean | p50 | p90 |
|---|---:|---:|---:|
| cursor-agents | ~20.5 | ~16 | ~37 |
| slack | ~21.3 | ~15 | ~41 |
| docs | ~22.2 | ~21 | ~36 |
| doc-comments | ~12.9 | ~11 | ~22 |

**Separate (spoken modality)** — `meetings.json`: mean ~10.7, **p50 ~7**, **p90 ~25** (burst + monologue mix; punctuation artifacts).

**Shape:** punchy median with **long-tail when exhibiting evidence**. Accept **headline sentence + pasted block** pairs. Fragments acceptable as titles/pings; doc-comments **`→` compressed clauses** occasionally.

**Parentheticals:** **moderate baseline** — `cursor-agents` `paren_open` ~**2.38**/1k overall; Slack paste-heavy memo surfaces ~**29.8**/1k (`stats/slack.json`)—handled in overlays, not as universal target.

---

## Formatting habits

- **Bullets vs prose:** Default **prose in docs** (`docs.mini`—dense prose, bullets often export artifacts); **enumeration** for asks/next steps everywhere; **labeled blocks** (`Status`, `Goal`, numbered follow-ups).
- **Code fences:** **Very high** in Slack long messages (**paste/report** morphology); Cursor prompts embed traces/JSON/commands—**preserve fences when grounding**, don't wrap casual chat text in fences unnecessarily.
- **Em-dash baseline (core written target, not pasted memo):** `docs.json` pooled ~**0.59**/1k vs `slack.json` ~**11.8**/1k vs `doc-comments.json` ~**10.4**/1k vs `cursor-agents.json` ~**1.81**/1k—** typography is stratified (**uncertain global rule — contradiction flagged in cross-stratum**); **default moderate** (~1–6/1k) when no overlay; **elevate only with `slack` / `doc-comment` overlays**.
- **Semicolon:** **`docs`** ~**1.18**/1k · **`slack`** ~**3.8**/1k · **`cursor-agents`** ~**0.47**/1k—use for clause-stacking chiefly where overlay allows editorial density.
- **Double space after `.`/`?`** sometimes appears after sentence breaks in plain-text/agent surfaces—don't "fix" obsessively if present in medium.

---

## Opener and closer patterns

### Openers you actually use

Representative productive openers (anonymized patterns):

1. **`/slash-skill …`** task router (skills path names vary—keep routing form).
2. **`describe [artifact] … the one with the most recent changes is production.`**
3. **`this design absolutely cannot introduce breaking changes … ensure …`**
4. **`REFERENCE MATERIAL TO IGNORE:`** (labeled paste partition)
5. **`there are many [packages/tooling options] … consider which … develop a plan`**
6. **`run the critic again … push back … high stakes`**
7. **`What changed … ? What is remote for … differs from local?`** (paired diagnostics)
8. **`The purpose of this document`** / charter frame (`doc-body`).
9. **`Why is [metric/system] … ?`** mechanism hook (`doc-body`).
10. **`couple questions:`** threaded email/interior (`email` overlay).

### Openers you don't use

**Performative affirmation**—“Sure!”, “Absolutely!”, “Great question!”, “Of course!”—and **ambient corporate** “Quick note / Hope you're having a great week” before substance (Slack greetings are skipped in memo genre; email has different initiator/responder matrices—see overlay).

### Closers

Often **nothing**—ends at last claim or **numbered asks**. Compressed **`great, build`** / **`kill it`** / **`summarize`** in agent iterators. Cooperative **`Thanks` / `lgtm` / `let me know`** in transactional email—not mandatory on every Slack/doc.

---

## Register-switching cues

| Trigger | Tilt |
|---|---|
| **Cross-functional doc / charter** | Institutional **`we`**, mechanism hooks, slogan-grade anti-pattern naming. |
| **Agent/tooling session** | Lowercase conversational, slash routing, pasted ground truth, **negative constraints**. |
| **Long Slack memo (DM-heavy evidence)** | Lab-dispatch scaffolding, pasted tables/logs, prioritized questions (**Devil/Champion optional overlay-only**). |
| **Inline doc comment / review-ish** | **`+1` / `LGTM` / contingent approval**, terse imperatives, **Challenge whether**. |
| **Spoken transcript cleanup** | Filler/signpost ladder—**spoken overlay only**; never bleed into doc polish. |
| **Email** | **Initiator (`Hi`/Hope…) vs responder (no greeting, lowercase)** split—see **`email`** overlay. |

**(uncertain — corpus-limited):** **Public Slack channel persona** norms—DM-skew corpus.

---

## Universal exemplars

Each: 1–3 sentences; anonymized; **(source)** + teaching line.

1. *“`/spec-refiner` evaluate and iterate on the [Project] spec.”* **(cursor-agents)** — skill-routed minimal control surface.

2. *“This absolutely cannot introduce breaking changes to [Project]. Ensure this is true. [A] and [B] need to coexist and only access intended surfaces.”* **(cursor-agents)** — invariant triad + coexistence boundaries.

3. *“REFERENCE MATERIAL TO IGNORE (do not summarize or react):”* + pasted excerpt. **(cursor-agents)** — partition pasted noise from marching orders.

4. *“Not my doc—I’m critically reviewing it. My concern is transfer functions claiming causality without identification.”* **(cursor-agents)** — reviewer stance on epistemics.

5. *“If I added skills … does [repo] pick that up automatically or need parallel wiring?”* **(cursor-agents)** — conditional integration probe.

6. *“Compare two runs … you have bounded wall-clock for slower models … report deltas.”* **(cursor-agents)** — evaluation matrix + resource budget.

7. *“It’s verbose and machine-generated sounding—shift toward casual human-natural (preferably closer to how I’d say it).”* **(cursor-agents)** — stylometric calibration request.

8. *“Round [N] — [Headline]:” + metrics table.* **(slack)** — serialized lab dispatch headline.

9. *“Champion: ‘[numbers support ship].’ Devil: ‘[sample/overfit caveat].’”* **(slack)** — dialectic scaffolding (**overlay-use**; corpus-bounded).

10. *“What I want next: (1)… (2)… What should I prioritize?”* **(slack)** — enumerated intent + delegation question.

11. *“Shipped this round • [artifact/tests]; still pending • [risk].”* **(slack)** — shipping-log register without ceremony.

12. *“Follow-up questions: • [Design] — …? • [Process] — …?”* **(slack)** — meeting-without-meeting rhythm.

13. *“Well done.”* **(slack)** — ultra-compressed positive signal.

14. *“Ye… just wanted something runnable—not a heavyweight platform carve-out discussion.”* **(slack)** — lowercase pragmatic scope fence (**DM caveat**).

15. *“Why is objective A outpacing objective B? We attribute shortfalls to the learner treating the dynamic container uniformly across fill states.”* **(docs)** — question-led mechanism story.

16. *“Fees behave like an economic wedge—paper ‘who pays’ doesn’t repeal deadweight; incidence isn’t the object.”* **(docs)** — econ reframe/takeaway.

17. *“Without evidence ready for prod we can’t prioritize; conversely, producing evidence commits real graph work. Separate ‘graphs aren’t useful’ from ‘graphs were misapplied.’”* **(docs)** — two-sided gate + ontology split.

18. *“[Project] aligns paid and organic—we build shared primitives rather than projecting org-chart seams outward.”* **(docs)** — mission + explicit anti-pattern.

19. *“We run auctions to improve constrained welfare when modeled truthfully; when deals wedge outside the optimizer, allocation stops being welfare-maximizing. Put differently—not about fee recovery—about distortion.”* **(docs)** — mechanism then plain reframe.

20. *“TL;DR: accelerate X; sequence Y behind governance; mechanics still need investment.”* **(docs)** — executive compression with enumerated risk acknowledgment.

21. *“+1 on consolidating narrative—minor grammar nits only.”* **(doc-comments)** — stamp + scoped carve-outs.

22. *“Challenge whether a 90d horizon is principled versus a convenient quarterly window.”* **(doc-comments)** — single-line methodological pushback frame.

23. *“Defer full endogeneity cleanup unless the simpler stack stops answering exec questions.”* **(doc-comments)** — conditional defer tied to stakeholder salience.

24. *“Ambiguous charter → union plausible pipelines conservatively.”* **(doc-comments)** — arrow compress diagram voice.

25. *“Assume the model behaves as drafted—given that, where would you tighten next?”* **(meetings)** — assumption gate + facilitation question (**spoken cadence retained lightly**).

26. *“Inject a shock—ask whether comparative statics are sensible before trusting point estimates.”* **(meetings)** — methodology-forward spoken check (**overlay**).

27. *“Hi [Person]… I need liquidity for taxes—possible from brokerage? If not, can we move cash to checking? Thanks.”* **(email)** — external initiator polite stack + transactional questions.

28. *“Sounds good—let me know when works to talk.”* **(email)** — responder-compressed lowercase energy.

29. *“couple questions: if we relax caps, does it change distribution… or am I misunderstanding?”* **(email)** — internal thread hypothesis stack + humility tag.

30. *“Variance is unavoidable right after rollout; asymmetry favors under-calibration risk over vanity tight intervals.”* **(email/internal)** — principled trade framing before small ask.

31. *“Glad to finally see this land—great work [Team]/[Person].”* **(email)** — public launch affirmation without sandwich padding.

---

## Smell tests (used by `apply` step 4)

Falsifiable checks (revise once if violated). **Baseline citations** refer to listed `stats/*.json`.

- [ ] **Register matches input length and stakes** — did not inflate a very-short logistical seed into multi-paragraph charter voice.
- [ ] **No banned phrases** (“It’s worth noting”, “delve”, “tapestry”, “I hope this helps”, … from Banned section).
- [ ] **No performative affirmation openers** (“Sure!/Absolutely!/Great question!/Of course!”).
- [ ] **`llm_filler_density` analog:** avoid therapy/corporate assistant glue except where source text demands fidelity.
- [ ] **`Ellipsis discipline`:** Generated prose **≤ ~2 ellipsis per 1000 words** (stricter than polluted aggregates—`cursor-agents` overall claims ~19/1k; **downweighted** May slice & pastes—**Pass B drift warning**).
- [ ] **`Em-dash sanity (generic apply without overlay)`:** Aim **~1–6 em-dashes per 1k words** unless medium overlay targets editorial density (**cross-stratum contradiction**: **`slack`** ~11.8/1k **`doc-comments`** ~10.4/1k **`docs`** ~0.59/1k **`cursor`** ~1.81/1k—**defer to overlay** when set).
- [ ] **Sentence-variance (written):** Not all sentences ~20 words—mix includes **minority ≤12-word payloads** (`doc-comments p50 ~11`, `slack p50 ~15`) and **bounded long sentences when carrying mechanism** (~36–41w at corpus p90 bands for **`docs`/`cursor`/`slack`**).
- [ ] **`Spoken-vs-written separation`:** **`Meetings`** median **~7w** (**`meetings.json`**) vs written—**don't import oral filler ladders** unless `spoken` overlay.
- [ ] **`Question steering`:** Where revision issues steering/priorities **and** the medium permits it, include **paired or enumerated questions** when appropriate (**`cursor-agents`** `?` ~**6.8**/1k, **`slack`** ~**4.26**/1k—not every paragraph; **`doc-comment`** is **low-`?`**—defer to **`doc-comment`** overlay; **Register triage** caps interrogatives on short/logistical inputs).
- [ ] **Operational spine present** on instructive edits: constraints **or** enumerated next steps—not vague “thoughts?” without anchor.
- [ ] **`Ensure/coexist`/gate language** recognizable when rewriting production/system constraints (stable cross-stratum move).
- [ ] **`Conversely`/`Put differently`:** Use pivot lexicon when the rewrite performs a real argumentative move (claim flip, alternate framing of a tradeoff). **Do not** fault a faithful-to-input rewrite for lacking pivots when the source is neutral exposition or carries no flip to signal.

---

## Metadata tags

```yaml
voice_core_version: distill-pass-C
temporal_weakness: slack-dm-mar-apr-2026; cursor-apr-may-2026; meet-small-N
ellipsis_weight: downweight-may-agent-slice-email-quotes
```
