---
name: spec-writer
description: Turns a Figma design export (design/<feature>.json) and a meeting transcript (meetings/*.vtt) into a draft requirement specification (specs/<feature>.md), locked behind PO approval before any build work starts. Use when a feature's design and kickoff discussion both exist and a spec hasn't been drafted yet.
---

# spec-writer

## Inputs (both required)

1. `design/<feature>.json` — produced by `scripts/figma_export.py`. Contains the frame's
   flattened node tree, extracted text strings, and style tokens. This tells you **what
   the screen looks like and says** — not what the team decided about scope.
2. `meetings/*.vtt` — a WebVTT transcript of the kickoff conversation. This tells you
   **what was actually agreed**: what's in scope, what's explicitly out, and anything
   left open. Treat the transcript as authoritative over your own assumptions about
   what a screen like this "usually" needs.

If either input is missing, stop and say so — do not draft a spec from the design alone,
and do not draft one from the transcript alone. The whole point of this fragment is that
both inputs are read together.

## What to produce

Write `specs/<feature>.md` with this structure:

```markdown
---
status: draft
feature: <feature>
inputs:
  design: design/<feature>.json
  transcript: meetings/<transcript-file>.vtt
---

# <Feature Name> — Requirement Specification

## Overview
2-3 sentences: what this screen/feature is and why it's being built now.

## Source Inputs
- Design: <frame name>, pulled from <figma_url>
- Transcript: <meeting file>, <one-line summary of who attended>

## In Scope
Only what the transcript explicitly confirmed, cross-referenced against what
actually appears in the design extract.

## Out of Scope
Anything the transcript explicitly excluded — state it, don't just omit it silently,
so a reviewer can see it was considered and deliberately deferred, not missed.

## User Stories
3-5 INVEST-style stories, each with acceptance criteria, grounded in the design's
actual text/components — don't invent fields, buttons, or states that aren't in
design/<feature>.json.

## Open Questions
Anything the transcript flagged as undecided. Do not guess an answer and do not
quietly drop the question — it belongs here, for the PO to resolve during approval.
```

## Hard rules

- **Never invent scope the transcript didn't confirm**, even if the design shows it
  (e.g. a "Forgot password?" link in the mock that the transcript says is visual-only
  this sprint stays visual-only in the spec — do not silently promote it to a working
  flow because it's visible in the design).
- **Every field/button referenced in a user story must trace back to `text_content`
  or a named node in `design/<feature>.json`.** If it doesn't appear there, it doesn't
  belong in this spec.
- **`status` starts as `draft` and stays `draft`.** Only a human flipping it to
  `approved` (via a merged PR, per the workflow this skill feeds into) changes that —
  never set it to `approved` yourself.
- Keep it lean — this is the same "high-value content only" discipline as CLAUDE.md
  itself. No pasted transcript text beyond short, attributed paraphrases.
