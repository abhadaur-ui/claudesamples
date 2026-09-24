---
feature: authentication-ui
inputs:
  design: design/authentication-ui.json
  transcript: meetings/auth-ui-kickoff.vtt
---

# Authentication UI — Requirement Specification

## Overview
This sprint builds the login screen UI and its auth check, based on the "Sign in" frame
in the Modern Login Page Figma mock. The Product Owner scoped this narrowly at kickoff:
only the login screen and the auth check that follows a submit — nothing downstream, and
no adjacent flows (password reset, account settings) that appeared in earlier decks.

## Source Inputs
- Design: "Sign in" frame (node `1:359`, "Background+Border+Shadow"), part of the
  "Cover" canvas, pulled from
  https://www.figma.com/design/ehm86HJ49MkaEuOzvITTpW/Modern-Login-Page-UI-Template--Free---Community-?node-id=1-202&p=f&t=WyXnJyfDpe7RRdgk-0
- Transcript: `meetings/auth-ui-kickoff.vtt`, kickoff call with Product Owner, Developer,
  and Tester.

## In Scope
- Login form with **Email** and **Password** fields (labels and `your@email.com`
  placeholder per the design's `text_content`).
- Primary **Sign in** button that triggers an auth check.
- On successful auth, route the user to the existing dashboard route (already built;
  out of scope to change it).
- **Forgot your password?** link — renders visually per the design, per PO confirmation
  it does not need to be wired to a real flow this sprint.
- **Sign up** link ("Don't have an account? Sign up") — renders per the design and
  points to a stub destination this sprint; the full sign-up screen/flow is not part of
  this build.

## Out of Scope
- Password-reset flow — explicitly deferred by the PO to a separate ticket next sprint.
- Account-settings screen — explicitly excluded, was only in an earlier deck.
- Any real destination behind the "Forgot your password?" link — visual only this
  sprint; wiring it up is part of the password-reset ticket.
- A fully built sign-up screen/form — the "Sign up" link only needs to point to a stub
  this sprint.
- Anything downstream of a successful login besides routing to the existing dashboard
  route (the dashboard itself is not part of this build).

## User Stories

### 1. Login with email and password
As a user, I want to enter my email and password and sign in, so that I can access the
dashboard.
- **Acceptance criteria:**
  - Form shows an "Email" label with a `your@email.com` placeholder input, and a
    "Password" label with a masked password input (per design nodes `1:362`–`1:366`,
    `1:368`, `1:373`–`1:375`).
  - A primary "Sign in" button (design node `1:383`) submits the form and triggers the
    auth check.
  - On successful auth, the user is routed to the existing dashboard route.

### 2. See a visually-present "Forgot your password?" link
As a user, I want to see a "Forgot your password?" link on the login screen, so that I
know a recovery path will exist, even though it isn't wired up yet.
- **Acceptance criteria:**
  - The link text "Forgot your password?" renders per the design (node `1:371`).
  - Clicking it does not need to navigate anywhere or trigger any flow this sprint.

### 3. See a "Sign up" link pointing to a stub
As a user without an account, I want a way to get to sign-up from the login screen, so
that I'm not stuck if I don't have credentials yet.
- **Acceptance criteria:**
  - The line "Don't have an account? Sign up" renders per the design (nodes `1:384`,
    `1:387`).
  - Clicking "Sign up" points to a stub destination — no built-out sign-up form is
    required this sprint.

### 4. Handle a failed login attempt
As a user, I want to know when my login attempt didn't succeed, so that I can try again.
- **Acceptance criteria:**
  - A failed auth check keeps the user on the login screen and surfaces an error.
  - Exact error granularity (generic vs. field-specific) is an open question — see below.

## Open Questions
- Should a failed login show one generic error, or distinguish "wrong password" from
  "unrecognized email"? The PO deferred this decision to spec review rather than guess
  at kickoff.
- The design also includes a "Remember me" checkbox and "Sign in with Google" /
  "Sign in with Facebook" buttons (nodes `1:378`, `1:392`–`1:403`), but these were not
  discussed at kickoff. Are they in scope for this sprint, or deferred like password
  reset?
