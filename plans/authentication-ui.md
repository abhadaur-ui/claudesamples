---
feature: authentication-ui
spec: specs/authentication-ui.md
---

# Authentication UI — Build Plan

## Summary
Builds the login screen and its client-side auth check against the approved
`specs/authentication-ui.md`, using the existing `frontend/authentication-ui/` files
as the implementation location.

## Checkpoints

1. **Static markup + styling** — `index.html` / `auth.css` render the "Sign in" card:
   Email field (`your@email.com` placeholder), Password field, primary "Sign in"
   button, "Forgot your password?" link, and the "Don't have an account? Sign up"
   line, matching the design's text and layout.
2. **Form validation** — `auth.js`'s `isFormValid` blocks submit when email or
   password is empty, before any network call is made.
3. **Auth check + routing** — `auth.js`'s `attemptLogin` posts to the auth endpoint;
   on success, navigate to the existing dashboard route; on failure, show an error
   and keep the user on the login screen. (Blocked/affected by the open question below
   — implement as a single generic error message, not per-field, until the PO decides.)
4. **Stub links** — "Forgot your password?" and "Sign up" render as static links with
   no wired-up navigation/flow, per spec.
5. **Unit tests** — `test_auth.js` covers validation and the success/failure branches
   of the auth check.

## Files touched
- `frontend/authentication-ui/index.html`
- `frontend/authentication-ui/auth.css`
- `frontend/authentication-ui/auth.js`
- `frontend/authentication-ui/test_auth.js`

## Test list
| # | Test | Spec acceptance criterion |
|---|---|---|
| 1 | Email + password labels/placeholder, masked password input, and "Sign in" button render | Story 1 |
| 2 | Empty email or empty password blocks submit (`isFormValid` false) | Story 1 |
| 3 | Successful auth check (`attemptLogin` → ok) routes to the existing dashboard route | Story 1 |
| 4 | "Forgot your password?" link renders and does not navigate or trigger a flow | Story 2 |
| 5 | "Don't have an account? Sign up" line renders and the link points to a stub, not a built form | Story 3 |
| 6 | Failed auth check keeps the user on the login screen and shows an error | Story 4 |

**Not tested (open question, not silently resolved):** whether the failed-login error
should be generic or field-specific (wrong password vs. unrecognized email) — current
implementation shows one generic message pending the PO's decision. No test asserts a
specific per-field error copy.

## Definition of done
- `node frontend/authentication-ui/test_auth.js` passes.
- Manual visual check of `index.html` against `design/authentication-ui.json` (fields,
  labels, button text, link text all match).
- No behavior added beyond the spec's In Scope section (no password-reset wiring, no
  built-out sign-up form, no dashboard changes).

## Out of scope (carried from spec)
- Password-reset flow — deferred to a separate ticket next sprint.
- Account-settings screen — explicitly excluded.
- Any real destination behind the "Forgot your password?" link.
- A fully built sign-up screen/form — the "Sign up" link only needs a stub.
- Anything downstream of a successful login besides routing to the existing dashboard
  route.
