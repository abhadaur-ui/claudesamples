#!/usr/bin/env python3
"""
.claude/hooks/require_approved_spec_and_plan.py

A PreToolUse hook. Claude Code runs this automatically before every Edit/Write/
MultiEdit call, feeding it a JSON description of the tool call on stdin. This
script reads that JSON, and if the edit targets real source code (backend/ or
frontend/), refuses to let it proceed unless BOTH specs/<feature>.md and
plans/<feature>.md are present on main (i.e. merged) — a merged PR is the
approval signal under the single-PR-approval model (see .claude/skills/
spec-writer and plan-writer). There is no `status:` front-matter field
anymore; do not reintroduce a check for one.

Exit code 0  -> allow the tool call
Exit code 2  -> block it; stderr is fed back to Claude as the reason

Feature name is taken from the current git branch (e.g. feature/authentication-ui
-> "authentication-ui"), matching the branch-naming convention from CLAUDE.md.
If the branch name can't be parsed, this fails CLOSED (blocks), not open —
an unknown feature is treated the same as an unapproved one.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

CODE_PREFIXES = ("backend/", "frontend/")


def current_feature_from_branch() -> str | None:
    # symbolic-ref works even on a brand-new branch with no commits yet
    # (rev-parse --abbrev-ref HEAD fails in that case: "unknown revision").
    # Fall back to rev-parse for detached-HEAD states, where symbolic-ref fails instead.
    for cmd in (["git", "symbolic-ref", "--short", "HEAD"],
                ["git", "rev-parse", "--abbrev-ref", "HEAD"]):
        try:
            branch = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
            if branch and branch != "HEAD":
                break
        except Exception:
            branch = None
    else:
        return None
    if not branch:
        return None
    m = re.match(r"^(?:feature|bugfix)/([a-zA-Z0-9\-]+)", branch)
    return m.group(1) if m else None


def is_merged_to_main(md_path: str) -> bool:
    # A file counts as "approved" once it exists on main - that merge IS the
    # approval under the single-PR-approval model, no status field to check.
    for ref in ("main", "origin/main"):
        try:
            subprocess.check_output(
                ["git", "cat-file", "-e", f"{ref}:{md_path}"],
                stderr=subprocess.DEVNULL,
            )
            return True
        except Exception:
            continue
    return False


def main():
    raw = sys.stdin.read()
    try:
        event = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        event = {}

    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")

    if tool_name not in ("Edit", "Write", "MultiEdit"):
        sys.exit(0)  # not a code-writing call this hook cares about

    if not any(file_path.startswith(p) for p in CODE_PREFIXES):
        sys.exit(0)  # not touching backend/ or frontend/ — nothing to gate

    feature = current_feature_from_branch()
    if not feature:
        print(
            "BLOCKED: could not determine feature from branch name "
            "(expected feature/<name> or bugfix/<name>). Refusing to write "
            f"to {file_path} without a known spec/plan to check against.",
            file=sys.stderr,
        )
        sys.exit(2)

    spec_merged = is_merged_to_main(f"specs/{feature}.md")
    plan_merged = is_merged_to_main(f"plans/{feature}.md")

    if not spec_merged or not plan_merged:
        print(
            f"BLOCKED: writing to {file_path} requires both "
            f"specs/{feature}.md and plans/{feature}.md to be merged to main.\n"
            f"  specs/{feature}.md  merged to main = {spec_merged}\n"
            f"  plans/{feature}.md  merged to main = {plan_merged}\n"
            "Both must land on main via a merged PR (the merge is the "
            "approval) before any code may be written for this feature.",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
