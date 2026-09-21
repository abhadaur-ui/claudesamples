---
name: pipeline-reset
description: Deletes specs/<feature>.md and plans/<feature>.md and pushes the removal directly to main, so the spec-writer -> plan-writer -> build pipeline can be replayed end to end for a demo. Leaves design/<feature>.json and meetings/*.vtt untouched. Use when the user asks to reset, replay, or re-run the pipeline demo for a feature.
---

# pipeline-reset

## What this does

Removes the two downstream artifacts that spec-writer and plan-writer produce,
so the human-approval-gate demo can be run again from the same design extract
and transcript:

- `specs/<feature>.md`
- `plans/<feature>.md`

It does **not** touch `design/<feature>.json` or `meetings/*.vtt` — those are
the upstream inputs and are reused as-is across replays. If the user wants a
full reset including a fresh Figma extract, that's a separate, explicit ask
(requires `FIGMA_TOKEN` and `scripts/figma_export.py`) — do not delete the
design JSON as part of this skill.

## Preconditions

- Ask for `<feature>` if it isn't given, or infer it if there's exactly one
  feature with both a spec and a plan present.
- `git status` must be clean before running — if there are uncommitted changes,
  stop and tell the user rather than resetting on top of unrelated work.

## Steps

1. `git status` — confirm clean working tree.
2. `git rm specs/<feature>.md plans/<feature>.md` (only remove the ones that
   exist — it's fine if one is already absent from a prior partial replay).
3. Commit directly to `main`:
   ```
   git commit -m "Reset <feature> spec/plan for pipeline demo replay"
   ```
4. `git push origin main`.

This is a direct push to `main`, not a PR — it's a demo-harness reset, not a
deliverable requiring review, matching the precedent in this repo's git history
(e.g. the original "Reset authentication-ui pipeline artifacts" commits).

## After reset

Tell the user the reset is done and that the next step is `/spec-writer`
(and, once that PR is merged, `/plan-writer`) — this skill only resets state,
it does not chain into drafting the spec itself.

## Hard rules

- Never delete `design/<feature>.json` or `meetings/*.vtt` — only the two
  generated artifacts.
- Never push straight to `main` for anything other than this reset — every
  other change in this pipeline (spec, plan, build) goes through a PR that a
  human merges.
- Never merge a PR as part of this or any other pipeline skill.
