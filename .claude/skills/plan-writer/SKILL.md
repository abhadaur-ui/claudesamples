---
name: plan-writer
description: Turns an approved requirement specification (specs/<feature>.md) into a build plan and test list (plans/<feature>.md), submitted as a PR for Dev + Tester review — the merged PR is the approval. Also files the spec's user stories to Jira. Use once a spec exists and has been merged to main.
---

# plan-writer

## Precondition — check this before doing anything else

Confirm `specs/<feature>.md` exists **on main** (i.e. its PR has been merged) —
**if it's only on a branch/PR that hasn't merged yet, stop immediately and tell
the user why**, no matter how confident it looks or how much the human asking
seems to want you to proceed. A spec awaiting review is not a spec you build
against. There is no `status` field to check — a merged spec PR is the only
approval signal.

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
feature: <feature>
spec: specs/<feature>.md
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

## Submitting for approval

Open one PR containing `plans/<feature>.md`. There is no `status` field and no
second "approval" PR — Dev + Tester reviewing and merging this PR **is** the
approval. Do not merge it yourself.

## After the plan PR is opened — file Jira stories

Once `plans/<feature>.md` is drafted and its PR is open, file the spec's user
stories to Jira (this happens once, when drafting the plan — not gated on the
plan PR merging, since Jira tracking should exist while the plan is under review):

1. Read `jira/config.json` for `cloud_id`, `project_key`, `issue_type`. If this
   file is missing, skip this section entirely and tell the user it needs to be
   created first — do not guess a project key.
2. Read `jira/<feature>.json` if it exists — an array of
   `{ "story_number": N, "key": "...", "summary": "..." }`. Skip any
   `story_number` already recorded there; this is what makes re-running
   `plan-writer` on the same feature safe (no duplicate tickets).
3. For each remaining `**N. As a ... I can ...**` block under the spec's
   `## User Stories` section: the bold line is the Jira `summary`; the
   given/when/then and acceptance bullets beneath it form the `description`.
   Create the issue with `mcp__claude_ai_Atlassian__createJiraIssue`
   (`cloudId`, `projectKey`, `issueTypeName` from `jira/config.json`). Never
   invent a story that isn't literally in that section.
4. Append the newly created `{story_number, key, summary}` entries to
   `jira/<feature>.json` (create the file if it didn't exist).
5. Report the created Jira keys to the user alongside the plan PR link.

## Hard rules

- **Never draft a plan for a spec that hasn't merged to main** — this is the one
  rule this skill exists to enforce; everything else is secondary to it.
- If the spec's Open Questions section isn't empty, the plan may proceed, but must
  flag which checkpoints are blocked or affected by each open question rather than
  quietly assuming an answer.
