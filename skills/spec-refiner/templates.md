# Spec Templates

The orchestrator selects a template based on the detected spec type. All templates share a common preamble and epilogue; the core sections diverge by type. For hybrid specs, merge core sections from multiple types.

## Shared Preamble

```markdown
# [Project Name] — Specification

**Type**: [software | product | scientific | agentic | general]
**Status**: [draft | in-review | final]
**Author**: [name]
**Date**: [YYYY-MM-DD]
**Last revised**: [YYYY-MM-DD]

---

## 1. Overview

### 1.1 Problem Statement
<!-- What problem does this solve? Why does it matter? Who feels the pain? -->

### 1.2 Goals
<!-- Concrete, measurable outcomes. What does success look like? -->

### 1.3 Non-Goals
<!-- What is explicitly out of scope? What will this NOT do? -->

### 1.4 Success Criteria
<!-- How will we know this succeeded? Quantitative where possible. -->

## 2. Background & Context

### 2.1 Current State
<!-- How does the world work today? What exists already? -->

### 2.2 Prior Art
<!-- What has been tried before — internally or externally? What can we learn from it? -->

### 2.3 Constraints & Dependencies
<!-- External systems, timelines, regulatory requirements, team capacity, budget. -->
```

## Shared Epilogue

```markdown
## N-2. Resolved Assumptions

<!-- Assumptions that were surfaced during refinement and explicitly resolved. -->
<!-- Format: | Assumption | Resolution | Source | -->

| # | Assumption | Resolution | Source |
|---|------------|------------|--------|
| 1 | | | |

## N-1. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| | | | |

## N. Open Questions

None — all questions resolved during specification.

<!-- If any remain, they are listed here with owner and target resolution date. -->
```

---

## Software / Architecture

Core sections between preamble and epilogue:

```markdown
## 3. Design

### 3.1 Architecture
<!-- High-level component diagram. What are the major pieces? How do they interact? -->
<!-- Include a diagram (mermaid, ASCII, or link to image). -->

### 3.2 Data Model
<!-- Entities, relationships, schemas. Include table/collection definitions if applicable. -->
<!-- Specify storage engine, indexing strategy, and data lifecycle. -->

### 3.3 API / Interface Design
<!-- Endpoints, RPCs, or function signatures. Request/response schemas. -->
<!-- Versioning strategy. Breaking vs. non-breaking change policy. -->

### 3.4 Key Algorithms & Logic
<!-- Non-trivial logic that needs to be specified. Business rules, state machines, etc. -->

## 4. Detailed Requirements

### 4.1 Functional Requirements
<!-- What the system must do. Use numbered requirements (FR-1, FR-2, ...). -->

### 4.2 Non-Functional Requirements
<!-- Performance, scalability, availability, latency targets. -->
<!-- Specify with numbers: "p99 latency < 200ms", "99.9% availability". -->

### 4.3 Edge Cases & Error Handling
<!-- What happens when things go wrong? Partial failures, invalid input, timeouts. -->
<!-- Specify expected behavior for each edge case. -->

### 4.4 Security Considerations
<!-- Authentication, authorization, data sensitivity classification. -->
<!-- Trust boundaries, input validation, secrets management. -->

## 5. Observability & Operations

### 5.1 Monitoring & Alerting
<!-- Key metrics to track. Alert thresholds. Dashboards needed. -->

### 5.2 Deployment & Rollback
<!-- Deployment strategy (blue-green, canary, rolling). Rollback procedure. -->
<!-- Feature flags, gradual rollout plan. -->

### 5.3 Runbooks
<!-- Operational procedures for common failure scenarios. -->

## 6. Implementation Plan

### 6.1 Phases & Milestones
<!-- Break the work into phases. What ships first? What can be parallelized? -->

### 6.2 Testing Strategy
<!-- Unit, integration, e2e, load testing. What coverage is expected? -->

### 6.3 Migration Plan
<!-- If replacing an existing system: data migration, traffic cutover, rollback triggers. -->
```

---

## Product Requirements

Core sections between preamble and epilogue:

```markdown
## 3. Users & Personas

### 3.1 Target Users
<!-- Who are the primary, secondary, and tertiary users? -->

### 3.2 Jobs-to-be-Done
<!-- What are users trying to accomplish? What are their motivations and frustrations? -->

### 3.3 User Journeys
<!-- Step-by-step flows for key scenarios. Include happy path and key alternatives. -->
<!-- Use numbered steps. Note decision points and branching. -->

## 4. Requirements

### 4.1 Functional Requirements
<!-- What the product must do. Use numbered requirements (REQ-1, REQ-2, ...). -->
<!-- Each requirement should have clear acceptance criteria. -->

### 4.2 Acceptance Criteria
<!-- How do we verify each requirement is met? Testable conditions. -->
<!-- Format: Given [context], When [action], Then [expected outcome]. -->

### 4.3 Prioritization
<!-- MoSCoW (Must/Should/Could/Won't) or similar framework. -->
<!-- What ships in v1 vs. later iterations? -->

## 5. Design Constraints

### 5.1 UX Principles
<!-- Design principles guiding the product. Accessibility requirements. -->

### 5.2 Platform & Device
<!-- Supported platforms, browsers, screen sizes, offline requirements. -->

### 5.3 Accessibility
<!-- WCAG level, assistive technology support, internationalization needs. -->

## 6. Measurement

### 6.1 KPIs & Success Metrics
<!-- Key performance indicators. Baseline and target values. -->

### 6.2 Analytics Instrumentation
<!-- What events need to be tracked? What funnels need to be measurable? -->

### 6.3 Success Thresholds
<!-- At what metric values do we consider this a success, neutral, or failure? -->

## 7. Launch Plan

### 7.1 Phasing & Rollout
<!-- Alpha, beta, GA stages. Who gets access when? -->

### 7.2 Feature Flags
<!-- Which features are gated? Rollout percentages and criteria for advancement. -->

### 7.3 Communication
<!-- Internal and external announcements. Documentation, training, support readiness. -->
```

---

## Scientific Inquiry

Core sections between preamble and epilogue:

```markdown
## 3. Research Questions & Hypotheses

### 3.1 Research Questions
<!-- Precise questions this inquiry aims to answer. -->

### 3.2 Hypotheses
<!-- Testable predictions. State both the hypothesis and the null hypothesis. -->
<!-- Specify direction (one-tailed vs. two-tailed) and expected effect size if known. -->

### 3.3 Predictions
<!-- Observable outcomes that would confirm or disconfirm each hypothesis. -->

## 4. Methodology

### 4.1 Design
<!-- Experimental, quasi-experimental, observational, survey, etc. -->
<!-- Justify the choice of design. -->

### 4.2 Variables
<!-- Independent variables (manipulated or observed). -->
<!-- Dependent variables (measured outcomes). -->
<!-- Controlled variables (held constant or adjusted for). -->
<!-- Operationalize each variable: how exactly is it measured? -->

### 4.3 Controls & Randomization
<!-- Control group/condition. Randomization strategy. Blinding (single, double, none). -->

## 5. Data Collection

### 5.1 Data Sources
<!-- Where does the data come from? Tables, APIs, surveys, instruments. -->

### 5.2 Sample Size & Power
<!-- Required sample size. Power analysis parameters (alpha, beta, effect size). -->
<!-- Justify the chosen sample size. -->

### 5.3 Collection Protocol
<!-- Step-by-step data collection procedure. Timing, frequency, duration. -->

### 5.4 Instruments & Measures
<!-- Tools, scales, questionnaires, or queries used. Reliability/validity of instruments. -->

## 6. Analysis Plan

### 6.1 Statistical Methods
<!-- Primary analysis method. Justify the choice. -->
<!-- Specify the model, test statistic, and decision rule. -->

### 6.2 Multiple Comparisons
<!-- How are multiple comparisons handled? Bonferroni, FDR, pre-registered contrasts. -->

### 6.3 Effect Size & Practical Significance
<!-- Minimum detectable effect. What effect size is practically meaningful? -->

### 6.4 Sensitivity & Robustness
<!-- Sensitivity analyses planned. What assumptions are tested? -->

## 7. Validity & Limitations

### 7.1 Threats to Internal Validity
<!-- Confounds, selection bias, maturation, history, instrumentation. -->
<!-- How each threat is addressed or acknowledged. -->

### 7.2 Threats to External Validity
<!-- Generalizability limitations. Population, setting, time. -->

### 7.3 Known Limitations
<!-- What this study cannot answer. Caveats for interpreting results. -->

## 8. Ethics & Compliance

### 8.1 Ethical Review
<!-- IRB/ethics board status. Protocol number if applicable. -->

### 8.2 Informed Consent
<!-- Consent procedures. Opt-in vs. opt-out. Data subject rights. -->

### 8.3 Data Handling
<!-- PII handling, anonymization, retention, access controls. -->
```

---

## Agentic Tools / AI Systems

Core sections between preamble and epilogue:

```markdown
## 3. Agent Design

### 3.1 Capabilities
<!-- What can the agent do? Enumerate specific abilities. -->

### 3.2 Boundaries & Limitations
<!-- What the agent explicitly cannot or should not do. Hard limits. -->

### 3.3 Interaction Model
<!-- Human-in-the-loop, autonomous, semi-autonomous? -->
<!-- When does the agent ask for human input? What triggers escalation? -->

### 3.4 Escalation & Approval Gates
<!-- What actions require human approval? What thresholds trigger escalation? -->

## 4. Components

### 4.1 Skills
<!-- Skill definitions with name, description, trigger conditions, and workflow. -->

### 4.2 Tools & Integrations
<!-- MCP tools, APIs, CLIs the agent uses. Access patterns and permissions. -->

### 4.3 Subagents
<!-- Worker agents, their roles, model assignments, and coordination patterns. -->

### 4.4 Prompts & Instructions
<!-- System prompt design. Key behavioral instructions. Tone and style. -->

## 5. Integration

### 5.1 External Systems
<!-- What systems does the agent interact with? Read/write access. -->

### 5.2 Data Sources
<!-- Where does the agent get information? Freshness, reliability, access control. -->

### 5.3 Output Artifacts
<!-- What does the agent produce? File formats, locations, naming conventions. -->

## 6. Safety & Guardrails

### 6.1 Failure Modes
<!-- How can the agent fail? Enumerate specific failure scenarios. -->

### 6.2 Containment
<!-- Blast radius limits. What prevents the agent from causing damage? -->

### 6.3 Fallbacks
<!-- What happens when the agent can't complete a task? Graceful degradation. -->

### 6.4 Hallucination Mitigation
<!-- How are factual claims grounded? Source citation requirements. -->

## 7. Evaluation

### 7.1 Test Scenarios
<!-- Concrete test cases with expected agent behavior. -->

### 7.2 Success Criteria
<!-- How do we know the agent works correctly? Metrics, spot checks, user feedback. -->

### 7.3 Regression Plan
<!-- How do we detect when changes break existing behavior? -->
```

---

## General

Core sections between preamble and epilogue. The "Detailed Specification" section is intentionally flexible — the orchestrator adapts its structure to the subject.

```markdown
## 3. Scope & Definitions

### 3.1 Key Terms
<!-- Define terms that must be unambiguous. Avoid jargon without definition. -->

### 3.2 Boundaries
<!-- What is included and excluded. Adjacent concerns that are out of scope. -->

### 3.3 Deliverables
<!-- Concrete artifacts this specification produces. -->

## 4. Detailed Specification
<!-- Core content. Structure this section to fit the subject matter. -->
<!-- The orchestrator will adapt headings based on what emerges during refinement. -->

## 5. Process & Workflow

### 5.1 Steps
<!-- Ordered steps or phases. Numbered for clarity. -->

### 5.2 Decision Points
<!-- Where choices must be made. Who decides? What are the criteria? -->

### 5.3 Handoffs
<!-- Where responsibility transfers between people, teams, or systems. -->

## 6. Compliance & Governance

### 6.1 Regulatory Requirements
<!-- Laws, regulations, or standards that apply. -->

### 6.2 Organizational Policy
<!-- Internal policies or guidelines that constrain the work. -->

### 6.3 Approvals
<!-- Who must approve? What is the approval process? -->
```
