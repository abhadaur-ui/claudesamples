---
feature: authentication-ui
spec: specs/authentication-ui.md
---

# Authentication UI — Build Plan

## Summary
Build plan for the approved `specs/authentication-ui.md`: a login screen (email +
password, "Sign in" button) that posts to the existing auth endpoint and routes to
the existing dashboard on success, with the "Forgot your password?" and "Sign up"
links present but unwired this sprint.

## Checkpoints
1. **Markup** — login card with "Sign in" heading, Email/Password labeled fields
   (`your@email.com` placeholder per design), "Forgot your password?" link, "Sign
   in" submit button, "Don't have an account? Sign up" line.
2. **Styling** — card layout matching the design's field/button treatment.
3. **Form logic** — client-side presence validation, POST to the auth endpoint,
   route to the dashboard route on success, show an error state on failure.
   *Affected by open question 1 (error-message granularity): implement as a single
   generic error message only; do not add per-cause messages until the PO decides.*
4. **Tests** — one assertion-based check per acceptance criterion below.

**Not a checkpoint this sprint** (open question 2): the design's "Remember me"
checkbox and "Sign in with Google"/"Sign in with Facebook" buttons are not built,
since the PO's scope walkthrough didn't mention them. Do not add them until that
question is resolved.

**Not a checkpoint this sprint** (open question 3): no separate signup screen is
built — only the stub "Sign up" link — since no signup screen design exists in
`design/authentication-ui.json`.

## Files touched
- `frontend/authentication-ui/index.html` — login form markup
- `frontend/authentication-ui/auth.css` — layout/styling
- `frontend/authentication-ui/auth.js` — validation, submit handler, routing
- `frontend/authentication-ui/test_auth.js` — assertion-based checks

These already exist from a prior pass and implement the login form, generic-error
submit flow (`AUTH_ENDPOINT` = `/api/login`, `DASHBOARD_ROUTE` = `/dashboard`, both
per spec's "already exist elsewhere" note), and matching tests — this plan's
checkpoints describe verifying/maintaining them against the spec, not building from
scratch.

## Test list
- Story 1 (sign in with email/password): `isFormValid` rejects empty email, empty
  password, and both empty; accepts both present — `test_auth.js`
- Story 2 (dashboard routing on success): `attemptLogin` returns true on a 2xx
  response; submit handler routes to `DASHBOARD_ROUTE` on success — `test_auth.js`
- Story 3 (Forgot-password link visible, unwired): markup contains the link text
  with no submit/navigation handler attached — manual/DOM check, no behavior to
  assert
- Story 4 (Sign up link visible, stub): markup contains the "Sign up" line as a
  stub link — manual/DOM check, no behavior to assert
- **No test written for inline-error granularity** (open question 1) — current
  behavior is intentionally generic-only; leave as-is until PO decides

## Definition of done
- `node frontend/authentication-ui/test_auth.js` passes (all assertions pass, no
  thrown errors)
- Manual check: login screen renders Email/Password fields, Forgot-password link,
  Sign in button, and Sign up line matching the design text content
- No Remember-me checkbox, social sign-in buttons, or built signup screen added

## Out of scope (carried from spec)
- Password-reset flow — separate ticket next sprint
- Account-settings screen
- Anything downstream of login (dashboard itself already exists)
- Wiring the "Forgot your password?" and "Sign up" links to real flows
