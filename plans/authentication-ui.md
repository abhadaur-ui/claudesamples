---
feature: authentication-ui
spec: specs/authentication-ui.md
---

# Authentication UI — Build Plan

## Summary
Builds the login screen described in the approved `specs/authentication-ui.md`:
email/password login with a visual-only "Forgot your password?" link and a
sign-up stub, wired to an existing `/api/login` endpoint and `/dashboard` route.
`frontend/authentication-ui/` already has a first pass (`index.html`, `auth.css`,
`auth.js`, `test_auth.js`) that matches the spec closely — this plan verifies it
against every acceptance criterion and closes the remaining gaps rather than
rebuilding it.

## Checkpoints

1. **Markup matches spec fields** — `index.html` has `Email` (placeholder
   `your@email.com`), `Password` (masked via `type="password"`), a "Sign in"
   submit button, "Forgot your password?" link, and "Don't have an account? Sign up"
   line. Already present; no changes expected, just a field-by-field check against
   `design/authentication-ui.json` text nodes.
2. **Forgot-password / sign-up links stay stubs** — confirm neither link has a JS
   click handler wiring it to a real flow (both are plain `<a href="#">` today,
   which satisfies "renders, not wired" per the spec).
3. **Auth check + redirect** — `auth.js` posts to `AUTH_ENDPOINT` (`/api/login`)
   and redirects to `DASHBOARD_ROUTE` (`/dashboard`) on success; on failure it
   shows the generic `#error-message`. Point both constants at the real paths
   when this is wired into the actual app router (currently a `ponytail:` comment
   flags this).
4. **Error messaging — blocked on Open Question** — spec leaves "generic vs.
   field-specific error" undecided. Keep the current single generic message;
   do not add wrong-password/unrecognized-email differentiation until the PO
   answers this during spec review. If they do, this checkpoint reopens.
5. **Tests** — add coverage for the acceptance criteria not yet exercised by
   `test_auth.js` (see Test list).

## Files touched
- `frontend/authentication-ui/index.html` — verify only, no changes anticipated.
- `frontend/authentication-ui/auth.css` — verify only.
- `frontend/authentication-ui/auth.js` — update `AUTH_ENDPOINT`/`DASHBOARD_ROUTE`
  only if the real app's paths differ from `/api/login` and `/dashboard`.
- `frontend/authentication-ui/test_auth.js` — extend with the additional cases below.

## Test list
- `isFormValid` returns true only when both email and password are non-empty —
  already covered in `test_auth.js`.
- Successful `/api/login` response redirects to `/dashboard` — needs a test;
  requires mocking `fetch` and `window.location`, which needs a DOM environment
  (e.g. jsdom) this repo doesn't currently have. **Not adding jsdom for one test**
  — verify this manually in a browser instead (open `index.html`, submit against
  a stubbed 200 response) per ponytail's no-new-dependency-for-a-few-lines rule.
- Failed `/api/login` response shows `#error-message` and does not redirect —
  same manual-verification note as above.
- "Forgot your password?" and "Sign up" links render but have no click handler —
  visual/manual check against the design screenshot, not a unit test.
- Error-message wording (generic vs. field-specific) — **do not test**, this is
  the open question from the spec; a test here would silently pick an answer
  the PO hasn't given.

## Definition of done
- `node frontend/authentication-ui/test_auth.js` passes (all assertions green).
- Manual check: `index.html` opened in a browser visually matches the design
  screenshot (`screenshot_url` in `design/authentication-ui.json`) for layout,
  colors, and copy.
- Manual check: successful and failed login responses behave as described in
  the Test list above.

## Out of scope (carried from spec)
- Password-reset flow — deferred to next sprint's ticket.
- Account-settings screen — excluded entirely for now.
- A built-out signup screen/form — only the stub link is in scope this sprint.
- Anything downstream of successful login (the dashboard itself).
- Social sign-in (Google/Facebook) and "Remember me" — present in the design
  frame but not confirmed in scope; excluded pending PO answer to the open question.
