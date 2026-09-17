#!/usr/bin/env bash
set -euo pipefail
BRANCH="$1"; FILE="$2"; TITLE="$3"; BODY="$4"
git checkout -B "$BRANCH"
git add "$FILE"
git commit -m "$TITLE" --allow-empty
git push -u origin "$BRANCH"
gh pr create --title "$TITLE" --body "$BODY" --base main --head "$BRANCH"
