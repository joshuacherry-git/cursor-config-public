# Swarm Pattern Catalog

Reference for all orchestration patterns available to the swarm-orchestrator.

---

## P1: Partner Review Loop

**When to use**: Any implementation task where correctness matters. This is the default quality pattern.

**Workers**: Implementer + Reviewer

**Flow**:
```
Orchestrator → Implementer (build) → Orchestrator → Reviewer (review)
    ↑                                                      |
    |          if FAIL: feed critique back                  |
    └──────────────────────────────────────────────────────-┘
    if PASS or max cycles reached: done
```

**Protocol**:
1. Spawn Implementer with the task and context.
2. Receive Implementer's output.
3. Spawn Reviewer with the original objective, constraints, and the Implementer's changes.
4. If Reviewer returns PASS: accept the work. Done.
5. If Reviewer returns FAIL: extract the CRITICAL findings, spawn a new Implementer with the original task + the reviewer's critique + instruction "Fix these specific issues: [list]". Increment cycle count.
6. **Max 3 cycles.** If still failing after 3 cycles, present the remaining issues to the user and ask how to proceed.

**Parallel variant**: if the task has multiple independent components, run multiple Implementer+Reviewer pairs in parallel.

---

## P2: Careful Execution

**When to use**: High-stakes single-file changes, surgical fixes, or changes where the blast radius must be minimal.

**Workers**: Implementer (single)

**Flow**:
```
Orchestrator (gather extensive context) → Implementer (precise task) → Orchestrator (verify)
```

**Protocol**:
1. Gather extra context: read the target file, its tests, its callers, its dependencies.
2. Write a highly constrained prompt with explicit boundaries ("modify ONLY lines 45-60", "do NOT change the function signature").
3. Spawn one Implementer.
4. After receiving output, the orchestrator personally verifies the change is within bounds. If not, retry with tighter constraints.

---

## P3: Test-Driven Development

**When to use**: New features with clear specifications, or when the user explicitly asks for TDD.

**Workers**: Tester (test-first mode) → Implementer → Tester (run mode)

**Flow**:
```
Orchestrator → Tester (write tests from spec) → Orchestrator → Implementer (implement to pass tests) → Orchestrator → Tester (run tests) → Orchestrator
    ↑                                                                                                                                        |
    |          if tests fail: feed failures back to Implementer                                                                               |
    └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────-┘
```

**Protocol**:
1. Spawn Tester in test-first mode with the specification/requirements.
2. Receive the test file(s).
3. Spawn Implementer with the task + the test files as constraints ("your code must pass these tests").
4. Spawn Tester in run mode to execute the tests.
5. If all pass: done.
6. If failures: spawn Implementer with the failure details. Retry up to 2 times.

---

## P4: Test Runner

**When to use**: After any implementation change, to verify nothing broke.

**Workers**: Tester (run mode)

**Flow**:
```
Orchestrator → Tester (run existing tests) → Orchestrator
    |                                            |
    if failures: route to Implementer            |
    └────────────────────────────────────────────-┘
```

**Protocol**:
1. Spawn Tester in run mode with the appropriate test command.
2. If all pass: report success.
3. If failures: analyze whether failures are caused by the recent changes or are pre-existing. Route change-related failures to an Implementer for fixing.

---

## P5: Next Steps Proposal

**When to use**: When the user wants to know what to do next, or when a task is too vague to execute directly.

**Workers**: Researcher

**Flow**:
```
Orchestrator → Researcher (explore current state) → Orchestrator → User
```

**Protocol**:
1. Spawn Researcher with a question about the current state of the area the user is interested in.
2. Receive the research report.
3. Synthesize the findings into a prioritized list of concrete next steps.
4. Present to the user for selection.

---

## P6: Fan-out / Fan-in

**When to use**: Tasks with 3+ independent subtasks that can run in parallel. Multi-file changes, bulk operations, implementing multiple functions.

**Workers**: Multiple Implementers (parallel)

**Flow**:
```
Orchestrator (decompose into N subtasks) → [Implementer_1, Implementer_2, ..., Implementer_N] (parallel) → Orchestrator (merge)
```

**Protocol**:
1. Decompose the task into N independent subtasks. Each subtask must have clear boundaries (different files, different functions, different modules).
2. For each subtask, prepare a worker prompt with the specific context for that subtask.
3. Spawn all N Implementers in a single message (parallel launch).
4. Receive all results.
5. Check for conflicts: if two workers modified the same file or made incompatible changes, resolve manually or spawn a follow-up Implementer.
6. Optionally follow with P4 (Test Runner) to verify the merged result.

**Boundary rules**: if subtasks are NOT truly independent (they share state, modify the same files, or one depends on another's output), do NOT use this pattern. Use P8 (Pipeline) or P9 (Scaffold-then-Fill) instead.

---

## P7: Best-of-N

**When to use**: When there are multiple valid approaches and you want to compare them. Algorithm design, architecture decisions, optimization problems.

**Workers**: Multiple Implementers (parallel, isolated)

**Flow**:
```
Orchestrator → [Implementer_A (approach 1), Implementer_B (approach 2), ...] (parallel) → Orchestrator → Reviewer (judge) → Orchestrator
```

**Protocol**:
1. Define 2-3 distinct approaches to the same problem.
2. Spawn one Implementer per approach, each with explicit instructions to use that specific approach. Use `best-of-n-runner` subagent_type for git worktree isolation when the approaches produce conflicting file changes.
3. Receive all results.
4. Spawn a Reviewer with all results and the criteria for judging (performance, readability, maintainability, correctness).
5. Accept the winner. Optionally, combine the best elements of multiple approaches.

---

## P8: Pipeline

**When to use**: Sequential tasks where each step depends on the previous step's output.

**Workers**: Varies (sequential)

**Flow**:
```
Orchestrator → Worker_1 → Orchestrator → Worker_2 → Orchestrator → Worker_3 → Orchestrator
```

**Protocol**:
1. Define the pipeline stages in order. Common pipelines:
   - **Research → Implement → Test → Review**: `Researcher → Implementer → Tester → Reviewer`
   - **Research → Plan → Implement**: `Researcher → (Orchestrator synthesizes plan) → Implementer`
   - **Implement → Validate → Fix**: `Implementer → Validator → Implementer (fix violations)`
2. Execute each stage, passing the previous stage's output as context to the next.
3. At each stage boundary, the orchestrator reviews the output before passing it forward. If a stage's output is insufficient, retry that stage before proceeding.

---

## P9: Scaffold-then-Fill

**When to use**: Greenfield features with multiple components that must integrate. Prevents integration conflicts by establishing contracts first.

**Workers**: Implementer (scaffold) → Multiple Implementers (fill, parallel)

**Flow**:
```
Orchestrator → Implementer (create skeleton/interfaces) → Orchestrator → [Implementer_1 (component A), Implementer_2 (component B), ...] (parallel) → Orchestrator
```

**Protocol**:
1. Spawn one Implementer to create the skeleton: interfaces, type definitions, file structure, API contracts, and stub implementations.
2. Review the skeleton. Verify interfaces are complete and consistent.
3. Decompose the fill work by component. Each component worker receives the skeleton + the specific component to implement.
4. Spawn all component Implementers in parallel.
5. Merge results. The skeleton ensures they integrate cleanly.
6. Optionally follow with P1 (Partner Review) on the integrated result.

---

## P10: Adversarial Debate

**When to use**: Architecture decisions, design trade-offs, or when there is genuine uncertainty about the best approach.

**Workers**: Two Reviewers (with opposing briefs)

**Flow**:
```
Orchestrator → [Reviewer_A (argue for X), Reviewer_B (argue for Y)] (parallel) → Orchestrator (synthesize decision)
```

**Protocol**:
1. Frame the decision clearly: what are the options, what are the evaluation criteria.
2. Spawn two Reviewers in parallel. Each receives a brief to argue FOR their assigned position and AGAINST the other. Include the same factual context for both.
3. Receive both arguments.
4. Synthesize: identify where they agree, where they disagree, and what the strongest arguments are on each side.
5. Make a decision or present the synthesis to the user if the decision requires domain knowledge you lack.

---

## P11: Research Swarm

**When to use**: When you need to understand a complex system before taking action. When context gathering has multiple independent angles.

**Workers**: Multiple Researchers (parallel)

**Flow**:
```
Orchestrator → [Researcher_1 (angle A), Researcher_2 (angle B), Researcher_3 (angle C)] (parallel) → Orchestrator (synthesize)
```

**Protocol**:
1. Identify 2-4 independent research angles. Examples:
   - Angle A: "What does the current implementation look like?"
   - Angle B: "What do the existing tests cover?"
   - Angle C: "What are the downstream consumers of this code?"
2. Spawn one Researcher per angle in parallel.
3. Receive all reports.
4. Synthesize into a unified understanding. Resolve any contradictions between reports.
5. Use the synthesized context to plan the next step (often feeding into P6, P8, or P9).

---

## P12: Guard Rail

**When to use**: When output must conform to a strict specification, contract, or schema. As a gate after any Implementer.

**Workers**: Any producer worker → Validator

**Flow**:
```
Orchestrator → Implementer → Orchestrator → Validator (check against spec) → Orchestrator
    ↑                                                                           |
    |          if FAIL: feed violations back to Implementer                     |
    └───────────────────────────────────────────────────────────────────────────-┘
```

**Protocol**:
1. Run the producer worker (Implementer, Tester, etc.).
2. Spawn Validator with the spec/contract and the output.
3. If PASS: accept.
4. If FAIL: spawn Implementer with the specific violations to fix. Max 2 retries.

---

## P13: Progressive Refinement

**When to use**: When "good enough" is the goal and you want iterative improvement. Writing documentation, optimizing code, improving error messages.

**Workers**: Implementer + Reviewer (iterative)

**Flow**:
```
Orchestrator → Implementer (draft v1) → Orchestrator → Reviewer (suggest improvements)
    → Orchestrator → Implementer (draft v2) → Orchestrator → Reviewer (suggest improvements)
    → ... (until diminishing returns or max iterations)
```

**Protocol**:
1. Spawn Implementer with the task. Mark it as "first draft — focus on correctness over polish."
2. Spawn Reviewer. Instead of PASS/FAIL, ask for "top 3 improvements that would have the most impact."
3. If improvements are substantial: spawn Implementer with the draft + improvements.
4. Repeat until Reviewer's suggestions are minor or you hit 3 iterations.
5. Accept the latest draft.

---

## P14: Speculative Execution

**When to use**: When the right approach is uncertain and trying is faster than analyzing. Debugging (try multiple hypotheses), migration (try multiple strategies).

**Workers**: Multiple Implementers (parallel, isolated)

**Flow**:
```
Orchestrator → [Implementer_A (hypothesis 1), Implementer_B (hypothesis 2)] (parallel)
    → Orchestrator → Tester (verify which one works) → Orchestrator (commit the winner)
```

**Protocol**:
1. Identify 2-3 possible approaches or hypotheses.
2. Spawn Implementers in parallel, each pursuing a different approach. Use `best-of-n-runner` subagent_type if the approaches produce conflicting file changes.
3. Spawn Tester to verify which solution actually works (passes tests, fixes the bug, etc.).
4. Commit the successful approach. Discard the others.

---

## P15: Red Team

**When to use**: Security-sensitive code, critical infrastructure, or when you want to proactively find failure modes.

**Workers**: Implementer → Reviewer (in red-team mode)

**Flow**:
```
Orchestrator → Implementer (build solution) → Orchestrator → Reviewer (try to break it)
    → Orchestrator → Implementer (harden against findings) → Orchestrator
```

**Protocol**:
1. Spawn Implementer to build the solution.
2. Spawn Reviewer with a red-team brief: "Your goal is to break this. Find edge cases that produce wrong results, inputs that cause crashes, sequences of operations that corrupt state, and security vulnerabilities. Write specific attack scenarios, not vague concerns."
3. Route the attack scenarios to a new Implementer to harden the solution.
4. Optionally repeat for a second round of red-teaming.

---

## Chaining Patterns

Complex tasks often require chaining multiple patterns. Common chains:

| Task Shape | Chain |
|---|---|
| Build a new feature with tests | P11 (Research) → P9 (Scaffold) → P3 (TDD) → P1 (Review) |
| Fix a bug | P11 (Research) → P14 (Speculative fix) → P4 (Test Runner) |
| Refactor across many files | P11 (Research) → P6 (Fan-out refactor) → P4 (Test Runner) → P1 (Review) |
| Architecture decision | P11 (Research) → P10 (Debate) → P9 (Scaffold) |
| Security hardening | P11 (Research) → P2 (Careful fix) → P15 (Red Team) → P2 (Harden) |
| Write documentation | P11 (Research) → P13 (Progressive Refinement) |
| Explore unfamiliar code | P11 (Research) → P5 (Next Steps) |
