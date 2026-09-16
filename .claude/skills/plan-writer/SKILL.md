---
name: plan-writer
description: Turns an approved requirement specification (specs/<feature>.md) into a build plan and test list (plans/<feature>.md), locked behind a second approval (Dev + Tester) before any code gets written. Use once a spec exists and its status has been confirmed approved.
---

# plan-writer

## Precondition — check this before doing anything else

Read `specs/<feature>.md`'s front-matter. **If `status` is not exactly `approved`,
stop immediately and tell the user why** — do not draft a plan against a spec that's
still `draft`, no matter how confident it looks or how much the human asking seems
to want you to proceed. A spec awaiting review is not a spec you build against.

This mirrors `spec-writer`'s own rule about never inventing scope: here, the
equivalent discipline is never skipping the approval check because it's inconvenient
or because the requester assumed it was already handled.

## Inputs (once the precondition passes)

1. `specs/<feature>.md` — the approved spec. This is the *only* source of scope.
   If something isn't in the spec's In Scope / User Stories sections, it doesn't
   belong in the plan, even if it seems like an obvious addition.
2. `design/<feature>.json` — for concrete field names, component names, and text
   labels, so the plan references real elements rather than paraphrasing.
3. The existing codebase — explore relevant files first (routers, existing
   components, conventions) before proposing file changes, same Explore-before-Plan
   discipline as everywhere else in this project.

## What to produce

Write `plans/<feature>.md`:

```markdown
---
status: draft
feature: <feature>
spec: specs/<feature>.md
spec_approved_at: <the spec's own approval, referenced not re-verified by you>
---

# <Feature Name> — Build Plan

## Summary
1-2 sentences referencing the approved spec by name.

## Checkpoints
Break the build into small, independently reviewable steps (data layer, then
endpoint/component, then wiring, then tests) — not one giant step. Each checkpoint
should be small enough that a reviewer can tell whether it matches the spec.

## Files touched
Concrete file paths, grounded in what you found exploring the codebase — not
guessed at.

## Test list
One test per acceptance criterion in the spec. If the spec has an Open Question,
do not write a test that silently resolves it — leave a note instead.

## Definition of done
Concrete and checkable: which commands must pass (lint, typecheck, tests), not
vague language like "code is clean."

## Out of scope (carried from spec)
Restate the spec's Out of Scope section here too, so a reviewer approving the
*plan* doesn't have to flip back to the spec to check the boundary is still intact.
```

## Hard rules

- **Never set `status` to `approved` yourself** — same rule as `spec-writer`. Only
  a human, via a merged PR, changes that.
- **Never draft a plan for an unapproved spec** — this is the one rule this skill
  exists to enforce; everything else is secondary to it.
- If the spec's Open Questions section isn't empty, the plan may proceed, but must
  flag which checkpoints are blocked or affected by each open question rather than
  quietly assuming an answer.
