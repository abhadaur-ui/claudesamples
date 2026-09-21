---
feature: authentication-ui
inputs:
  design: design/authentication-ui.json
  transcript: meetings/auth-ui-kickoff.vtt
---

# Authentication UI — Requirement Specification

## Overview
This sprint builds the login and signup screens from the "Login page" Figma mock, plus
the auth check that runs on login submission. It does not touch password reset,
account settings, or anything downstream of a successful login.

## Source Inputs
- Design: "Cover" frame ("Login page"), pulled from
  https://www.figma.com/design/ehm86HJ49MkaEuOzvITTpW/Modern-Login-Page-UI-Template--Free---Community-?node-id=1-202&p=f&t=WyXnJyfDpe7RRdgk-0
- Transcript: `auth-ui-kickoff.vtt` — kickoff call with Product Owner, Developer, and Tester

## In Scope
- Login screen with **Email** and **Password** fields (`Label → Email`, `Label → Password`
  in the design), matching the mock's "Sign in" heading and form layout.
- Primary **"Sign in"** button that submits the login form and runs the auth check.
- **"Forgot your password?"** link: renders visually per the mock, not wired to a real flow
  (PO: "Just visually present... doesn't need to be wired to a real flow this sprint").
- **"Sign up"** link/line at the bottom ("Don't have an account? Sign up"): renders per the
  mock and points to a stub for now (PO: "it can point to a stub for now").
- On successful login, route the user to the existing dashboard route (PO: "Route to the
  existing dashboard route, that part already exists").
- The signup screen itself (design extract only shows the login/"Cover" frame in detail;
  its fields/layout are the counterpart screen the PO referred to as "login and signup" —
  scope is confirmed, but no signup-specific design nodes are available in
  `design/authentication-ui.json` to spec field-by-field here).

## Out of Scope
- **Password-reset flow** — explicitly deferred: "Password reset is a separate ticket for
  next sprint. Don't build any of that yet." The "Forgot your password?" link stays
  visual-only.
- **Account-settings screen** — explicitly excluded per the earlier deck discussion: "leave
  those out entirely for now."
- **Anything downstream of login** beyond routing to the existing dashboard — the PO was
  explicit that only "the login/signup screen and the auth check itself" are in scope.
- **"Sign in with Google" / "Sign in with Facebook" buttons and the "Remember me" checkbox**
  — these appear in `design/authentication-ui.json` (nodes `1:392`–`1:403`, `1:378`) but were
  never discussed in the transcript. Per the PO's framing ("we only need the authentication
  UI built... Nothing else"), these are treated as not-yet-confirmed and excluded from this
  spec rather than silently built. Flagging for PO decision — see Open Questions.

## User Stories

**1. As a user, I can see and use a login form so I can access my account.**
- Given the login screen, I see fields labeled "Email" (placeholder "your@email.com") and
  "Password" (masked input).
- The form is contained under the "Sign in" heading.
- Acceptance: both fields are present and editable; submitting with both filled triggers
  the auth check.

**2. As a user, I can submit my credentials via a primary "Sign in" button.**
- Given valid-looking input in both fields, clicking "Sign in" runs the auth check.
- Acceptance: on successful authentication, the user is routed to the existing dashboard
  route. (Failure-state messaging is an open question — see below.)

**3. As a user, I can see a "Forgot your password?" link, understanding it doesn't do
anything yet.**
- Given the login screen, the "Forgot your password?" link renders in its mock position.
- Acceptance: the link is visible and styled per the mock but is not wired to any flow this
  sprint.

**4. As a user, I can see a way to switch to signup from the login screen.**
- Given the login screen, the "Don't have an account? Sign up" line renders at the bottom.
- Acceptance: "Sign up" is a visible link/stub target; it does not need to route to a fully
  built signup flow beyond the stub.

**5. As a user, I can access a signup screen as confirmed in scope for this sprint.**
- Acceptance: a signup screen exists and is reachable from the login screen's "Sign up"
  link. (Field-level acceptance criteria for signup are not specified here because no signup
  design nodes were present in `design/authentication-ui.json` — only the login/"Cover"
  frame was extracted. This should be confirmed with the PO/Figma file before build.)

## Open Questions
- **Error messaging on failed login**: should there be distinct inline errors for "wrong
  password" versus "unrecognized email," or a single generic error? PO explicitly deferred
  this: "let's flag that as open and decide it during spec review rather than guessing now."
- **Social sign-in buttons and "Remember me" checkbox**: these exist in the Figma mock but
  were not discussed in the kickoff. Are they in scope for this sprint, or deferred like
  password reset?
- **Signup screen design**: the design extract only contains the login ("Cover") frame in
  detail. Is there a separate Figma frame for signup that should be extracted before build
  starts?
