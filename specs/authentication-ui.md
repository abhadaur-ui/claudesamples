---
feature: authentication-ui
inputs:
  design: design/authentication-ui.json
  transcript: meetings/auth-ui-kickoff.vtt
---

# Authentication UI — Requirement Specification

## Overview
This sprint builds the login and signup screen UI based on the "Sign in" mock in Figma,
plus the auth check that runs on submit. Downstream screens (dashboard, password reset,
account settings) already exist or are separate tickets and are not part of this work.

## Source Inputs
- Design: "Cover" frame (node `1:339`, "Sign in" heading at `1:360`), pulled from
  https://www.figma.com/design/ehm86HJ49MkaEuOzvITTpW/Modern-Login-Page-UI-Template--Free---Community-?node-id=1-202&p=f&t=WyXnJyfDpe7RRdgk-0
- Transcript: `auth-ui-kickoff.vtt` — kickoff call with Product Owner, Developer, and Tester

## In Scope
- Login screen with Email and Password fields (design: `Label → Email` / `your@email.com`
  placeholder, `Label → Password` / masked input), and a primary "Sign in" button.
- "Forgot your password?" link — renders visually only, not wired to a flow this sprint.
- "Don't have an account? Sign up" link — points to a stub, not a working signup screen.
- On successful login, route to the existing dashboard route.
- The auth check itself (validating submitted credentials).

## Out of Scope
- Password-reset flow — explicitly deferred to a separate ticket next sprint.
- Account-settings screen — explicitly excluded, out of scope for this sprint.
- Any behavior downstream of a successful login beyond routing to the existing dashboard.
- Wiring the "Forgot your password?" and "Sign up" links to real flows — visual/stub only
  this sprint per PO.

## User Stories

### 1. View the login form
As a user, I want to see a login form with email and password fields so I can enter my
credentials.
- **Acceptance criteria:**
  - Screen displays "Sign in" heading (design: `1:360`).
  - Email field with label "Email" and placeholder "your@email.com" (design: `1:362`, `1:366`).
  - Password field with label "Password" and masked input (design: `1:368`, `1:375`).
  - Primary "Sign in" button is present (design: `1:383`).

### 2. Submit login credentials
As a user, I want to submit my email and password so I can be authenticated.
- **Acceptance criteria:**
  - Submitting the form runs the auth check against the entered email/password.
  - On success, the user is routed to the existing dashboard route.
  - On failure, an error is shown (see Open Questions for granularity).

### 3. See a visually-present "Forgot your password?" link
As a user, I want to see a "Forgot your password?" link so I know the option will exist,
even though it isn't functional yet.
- **Acceptance criteria:**
  - Link text "Forgot your password?" renders on the login screen (design: `1:371`).
  - Link is not wired to any flow this sprint.

### 4. Navigate toward signup via a stub
As a user without an account, I want a way to get to signup from the login screen.
- **Acceptance criteria:**
  - Text "Don't have an account?" and a "Sign up" link render on the login screen
    (design: `1:384`, `1:387`).
  - "Sign up" link points to a stub (no functional signup screen required this sprint).

## Open Questions
- Should login validation show distinct inline errors for "wrong password" vs.
  "unrecognized email," or a single generic error message? PO deferred this decision to
  spec review rather than guess.
- The design also includes "Remember me," "Sign in with Google," and "Sign in with
  Facebook" elements (design: `1:378`, `1:398`, `1:403`) that were not discussed on the
  call. Are these in scope for this sprint, or excluded like password reset?
