---
feature: authentication-ui
spec: specs/authentication-ui.md
---

# Authentication UI — Build Plan

## Summary
Build plan for the approved `specs/authentication-ui.md`: a login screen (email +
password, "Sign in" submit, visual-only "Forgot your password?" link, stubbed
"Sign up" link) that routes to the existing dashboard on success. The codebase
already has a skeleton at `frontend/authentication-ui/` that matches this shape;
checkpoints below complete and harden it rather than starting from scratch.

## Checkpoints
1. **Markup matches design** — confirm `index.html` has exactly the fields/labels/
   links named in `design/authentication-ui.json` (Email, Password, "Sign in",
   "Forgot your password?", "Don't have an account? Sign up") and nothing extra
   (no Remember me / social buttons — see Open Questions below).
2. **Client-side validation** — `isFormValid` blocks submit when email or password
   is empty (already present in `auth.js`); confirm it covers both fields independently.
3. **Auth call + routing** — form submit posts to the auth endpoint and, on success,
   redirects to the existing dashboard route; on failure, shows the error message
   element (blocked on the Open Question below for exact wording/granularity).
4. **Stub links stay inert** — "Forgot your password?" and "Sign up" render but do
   not trigger any flow beyond their stub target, per spec Out of Scope.
5. **Unit tests** — `test_auth.js` covers `isFormValid` truth table; add a test for
   the success/failure branching if not already covered.

## Files touched
- `frontend/authentication-ui/index.html` — markup for the fields/buttons/links.
- `frontend/authentication-ui/auth.css` — styling (no functional scope here).
- `frontend/authentication-ui/auth.js` — validation, auth call, and routing logic.
- `frontend/authentication-ui/test_auth.js` — unit tests.

## Test list
- Story 1 (sign in): valid email+password → authenticated and routed to dashboard.
- Story 1 (sign in): invalid credentials → error shown. **Blocked on Open Question**
  "error messaging granularity" — write the test against a single generic error for
  now, and flag it for revision once the PO decides, rather than guessing at distinct
  messages.
- Story 1 (validation): empty email or empty password → submit blocked, no request sent.
- Story 2 (forgot password): link renders on the login screen; selecting it triggers
  no reset flow this sprint.
- Story 3 (sign up): link renders; selecting it goes to the stub target, not a built
  sign-up screen.
- Story 4 (routing): successful login redirects to the existing dashboard route only
  (no new dashboard behavior asserted).

## Definition of done
- `node frontend/authentication-ui/test_auth.js` passes.
- Manual check of `index.html` in a browser: form renders per design, submit with
  empty fields is blocked, submit with the stub endpoint failing shows the error text.
- No Remember me checkbox or social sign-in buttons added until the corresponding
  Open Question is resolved by the PO.

## Out of scope (carried from spec)
- Password-reset flow — separate ticket next sprint.
- Account-settings screen — excluded entirely.
- Anything downstream of login besides the dashboard redirect.
- A fully built sign-up screen — stub link only.

## Open questions carried from spec (checkpoints affected)
- **Error messaging granularity** — affects Checkpoint 3 and its test; implemented
  with one generic error message for now, revisit once decided.
- **Remember me checkbox / social sign-in buttons** — affects Checkpoint 1; not built
  until the PO confirms whether they're in scope, visual-only, or omitted.
