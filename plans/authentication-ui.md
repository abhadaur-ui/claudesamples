---
feature: authentication-ui
spec: specs/authentication-ui.md
---

# Authentication UI — Build Plan

## Summary
Implements the login screen (and a stub signup screen) approved in
`specs/authentication-ui.md`: an email/password form with a "Sign in" submit
button, a visual-only "Forgot your password?" link, and a "Sign up" link that
points to a stub — nothing downstream of the auth check itself.

## Checkpoints
1. **Login markup + styles** — `frontend/authentication-ui/index.html` and
   `auth.css` already exist from a prior pass and match the mock (email field,
   password field, "Sign in" heading/button, "Forgot your password?" link,
   "Don't have an account? Sign up" line). Reviewer checks these against
   `design/authentication-ui.json` node text (`1:362`, `1:368`, `1:371`,
   `1:383`, `1:384`, `1:387`) before building further on top.
2. **Login submit + auth check wiring** — `frontend/authentication-ui/auth.js`
   already wires form submit to `AUTH_ENDPOINT` ("/api/login") and redirects to
   `DASHBOARD_ROUTE` ("/dashboard") on success, per the spec's routing
   requirement. Reviewer confirms these constants point at the real app's
   existing login-check endpoint and dashboard route when this is wired into
   the actual app (currently placeholder paths, flagged inline as a `ponytail:`
   comment).
3. **Forgot-password / sign-up links stay inert** — confirm `<a href="#">`
   placeholders for "Forgot your password?" and "Sign up" are not wired to any
   flow, matching the spec's Out of Scope section.
4. **Signup screen (stub)** — `design/authentication-ui.json` has no signup-
   specific nodes (only the "Cover"/login frame was extracted), so there's no
   design source to build a full signup screen against yet. This checkpoint is
   **blocked by the spec's own Open Question** ("Signup screen design" — no
   signup frame extracted). Until that's resolved, the "Sign up" link may point
   to a placeholder route/page with no defined fields — do not invent signup
   fields.
5. **Failed-login messaging** — `auth.js` currently shows one generic error
   message (`#error-message`, "Login failed. Please check your email and
   password.") on any non-OK response. This checkpoint is **blocked by the
   spec's Open Question** on whether distinct inline errors are needed per
   failure type. Until the PO decides, the generic message is a holding
   pattern, not a final answer — do not add per-field error branching without
   that decision.
6. **Tests** — `frontend/authentication-ui/test_auth.js` already covers
   `isFormValid` (client-side required-field validation). Extend only for new
   testable logic introduced in checkpoints above, not for the open-question
   items.

## Files touched
- `frontend/authentication-ui/index.html` — login form markup (existing, verify against design)
- `frontend/authentication-ui/auth.css` — styling (existing, verify against design)
- `frontend/authentication-ui/auth.js` — submit handler, auth check call, redirect (existing, verify endpoint/route wiring)
- `frontend/authentication-ui/test_auth.js` — unit tests for form validation (existing, extend if logic changes)
- A new signup screen file/route — not yet created; blocked on the Open Question above

## Test list
Mapped to `specs/authentication-ui.md` User Stories:
1. Login form renders email + password fields → `test_auth.js` structural check (existing `isFormValid` cases cover required-field behavior).
2. "Sign in" button submits and routes to dashboard on success → test that a mocked 2xx `/api/login` response redirects to `/dashboard`.
3. "Forgot your password?" renders but is not wired → test/assert the link has no live handler (e.g., still an `href="#"` or equivalent non-functional target).
4. "Sign up" link renders and points to a stub → test/assert the link exists and targets the stub, not a live signup submission.
5. Signup screen reachable — **no test written**; blocked on the Open Question about missing signup design. Do not write a test that assumes specific signup fields.
6. Failed-login error message — **no test asserting error-message content/granularity** beyond "an error is shown on non-OK response"; the wording/granularity question is open and untested by design, not by oversight.

## Definition of done
- `node frontend/authentication-ui/test_auth.js` passes.
- Manual check: `index.html` renders in a browser and visually matches
  `design/authentication-ui.json` text nodes for the login screen.
- No code added for the two Open-Question items beyond the documented holding
  pattern (generic error message, no signup fields invented).
- This plan and the spec PR are both merged to main before any further
  frontend/backend edits proceed (enforced by
  `.claude/hooks/require_approved_spec_and_plan.py`).

## Out of scope (carried from spec)
- Password-reset flow — deferred to a separate ticket next sprint.
- Account-settings screen — excluded entirely.
- Anything downstream of login besides the redirect to the existing dashboard route.
- "Sign in with Google" / "Sign in with Facebook" buttons and the "Remember me"
  checkbox — present in the Figma mock but never confirmed in scope; excluded
  pending PO decision (see spec Open Questions).
