# Fragment Pilot: Steps 1–3 (Extract → Spec)

This is a working pilot of the first three steps from *Figma-to-PR Fragment: Workflow
Design*, built to prove out direct-API extraction (no live Figma MCP) and a
transcript+design spec draft, before handing off to the rest of that deck's flow
unchanged.

## What's in this folder

```
scripts/figma_export.py        Step 1 — direct-API Figma extraction (not MCP)
test_figma_export.py           Proves the parsing logic (mock API response —
                                no live FIGMA_TOKEN in this environment)
design/authentication-ui.json  Step 1 output — static, one-time extract
meetings/auth-ui-kickoff.vtt   Step 2 input — kickoff call transcript
.claude/skills/spec-writer/    Step 3 skill definition — the rules Claude follows
  SKILL.md                     to turn (design + transcript) into a spec
specs/authentication-ui.md     Step 3 output — the draft spec, status: draft
```

## How each step maps to the deck (slide numbers refer to the attached PDF)

| # | Step | What ran | Slide |
|---|---|---|---|
| 1 | Extract | `figma_export.py` pulls one frame via Figma's REST API once, writes `design/<feature>.json`. No MCP connection stays open. | 4 |
| 2 | Spec inputs | A VTT transcript (`meetings/auth-ui-kickoff.vtt`) supplies scope decisions the design alone can't — what's in, what's deferred, what's still open. | — (new) |
| 3 | Spec drafted | The `spec-writer` skill combines both inputs into `specs/authentication-ui.md`, `status: draft`. | 3 (step 2) |

## Running step 1 for real

```bash
export FIGMA_TOKEN=figd_your_personal_access_token
python scripts/figma_export.py "https://www.figma.com/design/<file_key>/<name>?node-id=<id>" authentication-ui
```

This sandbox has no live `FIGMA_TOKEN`, so `test_figma_export.py` proves the same
parsing code against a mock API response shaped like a real "Login" frame instead —
run it yourself to see the exact node walk and text/style extraction that a live
call would also produce.

## From here: unchanged

Everything from **step 3 onward is exactly the proposed flow already agreed** —
nothing about using a transcript + design instead of design alone changes the rest
of the pipeline:

1. **PO approves** — `specs/authentication-ui.md` gets opened as a PR; the PO reviews
   it like any PR and flips `status: draft` → `status: approved` on merge (slide 5).
2. **Plan + tests drafted** — Claude reads the now-approved spec, drafts
   `plans/authentication-ui.md` against it.
3. **Dev/QA approve** — same PR-review pattern, second gate (slide 5).
4. **Build** — the `PreToolUse` hook checks both files say `approved` before any
   Edit/Write is allowed (slide 6).
5. **Tests run, PR raised** — CI, then a normal PR linking spec + plan as evidence
   (slide 8).

The manual-trigger recommendation also carries over unchanged: a developer kicks off
each next step by hand for now — no GitHub Actions wiring until this has run cleanly
a few times (slide 8, "Day one: manual trigger").
"# test" 
