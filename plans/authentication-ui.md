---
feature: authentication-ui
spec: specs/authentication-ui.md
---

# Authentication UI — Build Plan

## Summary
Implements the login/signup screen from the approved `specs/authentication-ui.md`:
email/password sign-in, a visual-only "Forgot your password?" link, a stub
"Sign up" link, and routing to the existing dashboard on success.

## Checkpoints
1. **Markup** — `frontend/authentication-ui/index.html`: email + password
   fields, "Forgot your password?" link, primary "Sign in" button, and the
   "Don't have an account? Sign up" line, matching the design's text content.
2. **Styling** — `frontend/authentication-ui/auth.css`: layout/visual styling
   for the card, form fields, and buttons per the Figma mock's style tokens.
3. **Auth wiring** — `frontend/authentication-ui/auth.js`: form validation
   (`isFormValid`), login submission (`attemptLogin` against `/api/login`),
   and redirect to `/dashboard` on success; generic error message on failure.
4. **Tests** — `frontend/authentication-ui/test_auth.js`: assertion-based
   checks for validation and login outcomes.

Existing files already implement checkpoints 1-4, consistent with this plan;
this plan documents them against the spec's acceptance criteria for review.

## Files touched
- `frontend/authentication-ui/index.html`
- `frontend/authentication-ui/auth.css`
- `frontend/authentication-ui/auth.js`
- `frontend/authentication-ui/test_auth.js`

## Test list
- Story 1 (sign in with email/password): `isFormValid` rejects empty
  email/password; `attemptLogin` returns true on a 2xx response and false
  otherwise (covered in `test_auth.js`).
- Story 1 (auth check failure): submitting invalid credentials shows the
  generic error message (`#error-message`) instead of navigating away.
- Story 2 ("Forgot your password?" link): link renders in the form and is
  not wired to a real flow — no test asserts navigation behavior for it.
- Story 3 (navigate toward sign up): "Sign up" link is present and points to
  a stub destination, not a built sign-up flow.
- Story 4 (land on dashboard after login): `attemptLogin` success redirects
  to `DASHBOARD_ROUTE` (`/dashboard`).

**Open Question carried over — not resolved by this plan:** whether login
errors should be split into per-cause messages (wrong password vs.
unrecognized email) or stay a single generic message. Current implementation
uses a single generic error (`auth.js`, marked with a `ponytail:` comment) as
a placeholder pending the PO's decision in spec review; no test locks in
per-cause messaging until that's resolved.

## Definition of done
- `node frontend/authentication-ui/test_auth.js` passes.
- Manual check: submitting valid credentials in `index.html` redirects to
  `/dashboard`; invalid credentials show the generic error message.
- No changes needed outside `frontend/authentication-ui/` for this scope.

## Out of scope (carried from spec)
- Password-reset flow — deferred to a separate ticket next sprint.
- Account-settings screen — explicitly excluded from this sprint.
- Anything downstream of the login/signup screen and the auth check itself
  (e.g. dashboard behavior).
