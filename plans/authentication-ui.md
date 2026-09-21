---
feature: authentication-ui
spec: specs/authentication-ui.md
---

# Authentication UI — Build Plan

## Summary
Implements the login screen and auth check described in the approved
`specs/authentication-ui.md`, plus the visual-only "Forgot your password?" and
"Sign up" stub links. `frontend/authentication-ui/` already contains a working
first pass (`index.html`, `auth.css`, `auth.js`, `test_auth.js`) from a prior
build — this plan verifies it against the spec and lists the remaining gaps.

## Checkpoints
1. **Markup** — `index.html` already has the Email/Password fields, "Sign in"
   heading and button, "Forgot your password?" link, and "Don't have an
   account? Sign up" line. Confirm labels/placeholders match
   `design/authentication-ui.json` (`your@email.com` placeholder, masked
   password). No changes expected here.
2. **Client-side validation + submit wiring** — `auth.js` already posts to
   `AUTH_ENDPOINT` and routes to `DASHBOARD_ROUTE` on success. Confirm both
   constants point at the real `/api/login` and `/dashboard` routes once wired
   into the actual app (currently marked with a `ponytail:` comment as a
   placeholder).
3. **Error handling** — **blocked on the spec's open question** (inline
   "wrong password" vs. "unrecognized email" errors, or one generic message).
   `auth.js` currently shows one generic error message on any non-2xx
   response. Do not change this ahead of the PO's answer; if the PO chooses
   inline errors, this checkpoint reopens.
4. **Stub links** — confirm "Forgot your password?" and "Sign up" remain
   non-functional (`href="#"`), per spec's Out of Scope.
5. **Tests** — `test_auth.js` already covers `isFormValid`. Add nothing further
   until the error-message open question resolves.

## Files touched
- `frontend/authentication-ui/index.html`
- `frontend/authentication-ui/auth.css`
- `frontend/authentication-ui/auth.js`
- `frontend/authentication-ui/test_auth.js`

## Test list
1. Login screen renders "Sign in" heading, Email field (placeholder
   `your@email.com`), Password field (masked), and "Sign in" button — covered
   by manual/visual check of `index.html` (no dedicated test file needed for
   static markup).
2. `isFormValid(email, password)` returns `true` only when both are
   non-empty — covered by `test_auth.js`.
3. Successful login (`/api/login` returns ok) redirects to `/dashboard` —
   not yet covered; add once `auth.js` is wired to a real endpoint (mocking
   `fetch`).
4. Failed login shows an error message — not yet covered; **do not lock down
   the exact error copy/granularity in a test until the open question is
   resolved.**
5. "Forgot your password?" and "Sign up" links render but are non-functional
   (`href="#"`) — covered by manual/visual check.

## Definition of done
- `node frontend/authentication-ui/test_auth.js` passes.
- Manual check of `index.html` in a browser matches the design's text labels.
- No changes made to error-message behavior until the PO resolves the open
  question in `specs/authentication-ui.md`.

## Out of scope (carried from spec)
- Password-reset flow — separate ticket next sprint.
- Account-settings screen.
- Any behavior downstream of a successful login beyond routing to the
  existing dashboard.
- Wiring "Forgot your password?" and "Sign up" to real flows.
- Remember me / Google / Facebook sign-in — not confirmed in scope (spec open
  question); do not build until PO answers.
