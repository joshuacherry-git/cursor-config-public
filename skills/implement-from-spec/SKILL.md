---
name: implement-from-spec
description: >-
  Sprint-style implementation from a specification file. Decomposes the spec
  into phases, scaffolds tests, implements incrementally with commits between
  milestones, and tracks progress. Use when the user says "implement this spec",
  "build from spec", "implement from spec", "start implementation", "code this
  up from the spec", or has a spec/PRD they want turned into working code.
---

# Implement from Spec

Turn a specification document into working code through structured, incremental implementation with test coverage and progress tracking.

## Workflow

### 1. Read and analyze the spec

- Read the spec file the user references (or find it in `~/code/specs/` if they mention a project name).
- Identify the target repository and working directory.
- Extract:
  - **Scope**: what the spec covers end-to-end
  - **Components**: distinct modules, classes, or files to create/modify
  - **Dependencies**: what each component depends on (ordering constraints)
  - **Acceptance criteria**: how to verify the implementation is correct
  - **Out of scope**: what the spec explicitly excludes

### 2. Decompose into phases

Break the spec into 2-5 implementation phases. Each phase should be:
- **Independently committable** — the codebase is in a valid state after each phase
- **Testable** — each phase has concrete verification (tests, manual check, or type-check)
- **Ordered by dependency** — earlier phases produce interfaces that later phases consume

Common phase patterns:
- **Phase 1**: Core data models / types / interfaces
- **Phase 2**: Business logic / main implementation
- **Phase 3**: Integration points / API surface
- **Phase 4**: Edge cases, error handling, polish
- **Phase 5**: Documentation, configuration, cleanup

For each phase, list:
- Files to create or modify
- What "done" looks like
- Estimated complexity (small / medium / large)

### 3. Present the plan

Show the user the phase breakdown before coding:

```
## Implementation Plan — {spec name}

### Phase 1: {title}
- Files: list of files
- Deliverable: what this phase produces
- Tests: what tests will verify this phase

### Phase 2: {title}
...

Estimated phases: N | Approach: {sequential / parallel where independent}
```

Wait for user confirmation. Incorporate feedback on ordering, scope, or approach.

### 4. Execute phase by phase

For each phase:

1. **Read existing code** in the target files (if modifying existing code). Understand the current patterns, imports, and conventions.
2. **Write tests first** when the phase has clear input/output contracts. Place tests alongside existing test files following the repo's conventions.
3. **Implement the code.** Follow the repo's existing style (naming, imports, error handling, type annotations).
4. **Run tests** to verify the phase. Fix any failures before proceeding.
5. **Run linters** on modified files. Fix introduced errors.
6. **Commit** with a descriptive message:
   ```
   feat(component): phase N — what this phase accomplished

   Part of {spec-name} implementation.
   ```

After each phase, briefly report what was completed and what's next.

### 5. Handle blockers

When a phase hits a blocker (missing dependency, ambiguous spec, environment issue):

1. **State the blocker clearly** — what's blocked and why.
2. **Propose options** — workaround, skip and return later, or ask the user for clarification.
3. **Do not silently skip** — if a spec requirement can't be implemented, flag it explicitly.
4. **Track skipped items** — maintain a running list of deferred work to present at the end.

### 6. Final verification

After all phases are complete:

1. Run the full test suite for the affected area.
2. Verify all acceptance criteria from the spec are met. For each criterion, note PASS or FAIL with evidence.
3. List any spec requirements that were deferred or partially implemented.

### 7. Summary

Present a completion summary:

```
## Implementation Complete — {spec name}

### What was built
- Component A: description
- Component B: description

### Commits
1. {hash} — Phase 1: description
2. {hash} — Phase 2: description

### Acceptance Criteria
- [x] Criterion 1 — verified by test_foo
- [x] Criterion 2 — verified by manual check
- [ ] Criterion 3 — deferred: reason

### Deferred / Follow-up
- Item that wasn't implemented and why
```

## Guidelines

- **Commit early, commit often.** Each phase gets its own commit. If a phase is large, consider mid-phase commits at natural boundaries.
- **Don't gold-plate.** Implement what the spec says. If you see opportunities for improvement beyond the spec, note them as ideas but don't implement unless asked.
- **Preserve existing patterns.** Match the repo's existing code style, test framework, and project structure. Don't introduce new patterns without asking.
- **Keep the user in the loop.** After each phase, report progress. Don't go silent for multiple phases.
- **Test coverage is not optional.** Every phase that introduces behavior should have tests. If the repo has no test infrastructure, set it up in Phase 1.
