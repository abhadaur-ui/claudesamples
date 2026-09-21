---
status: approved
feature: authentication-ui
inputs:
  design: design/authentication-ui.json
  transcript: meetings/auth-ui-kickoff.vtt
---

# Authentication UI — Requirement Specification

## Overview
A login and signup UI for the product, built from the "Modern Login Page UI Template" Figma mock. This sprint covers only the authentication screens and the auth check itself — nothing downstream or adjacent (password reset, account settings) is in scope.

## Source Inputs
- Design: "Cover" frame (node 1:202), pulled from https://www.figma.com/design/ehm86HJ49MkaEuOzvITTpW/Modern-Login-Page-UI-Template--Free---Community-?node-id=1-202
- Transcript: `auth-ui-kickoff.vtt` — kickoff call with Product Owner, Developer, and Tester

## In Scope
- Login screen with Email and Password fields (labels "Email" / "Password", placeholder "your@email.com")
- Primary "Sign in" button
- "Forgot your password?" link — renders visually only, not wired to a flow this sprint
- "Don't have an account? Sign up" link — points to a stub for now
- Successful login routes to the existing dashboard route (dashboard itself is out of scope)
- The auth check for login itself

## Out of Scope
- Password-reset flow — explicitly deferred to a separate ticket next sprint
- Account-settings screen — explicitly excluded from this ticket
- Anything downstream of a successful login beyond routing to the existing dashboard
- Wiring the "Forgot your password?" and "Sign up" links to real flows — visual/stub only this sprint
- "Remember me" checkbox and "Sign in with Google" / "Sign in with Facebook" buttons — present in the design mock but not mentioned in the kickoff scope discussion; not confirmed as in-scope functionality this sprint

## User Stories

**1. As a user, I can enter my credentials and sign in.**
- Given the login screen, I see labeled "Email" and "Password" fields (placeholder "your@email.com" for email)
- When I submit valid credentials via the "Sign in" button, I am routed to the existing dashboard route
- When credentials are invalid, an error is shown (exact messaging: see Open Questions)

**2. As a user, I can see a "Forgot your password?" link.**
- Given the login screen, the "Forgot your password?" link is rendered
- When I click it, no working flow is required this sprint (visual only)

**3. As a user, I can see a path to sign up.**
- Given the login screen, "Don't have an account? Sign up" is rendered
- When I click "Sign up", it points to a stub (no working signup screen required yet, since no signup screen design has been provided — see Open Questions)

## Open Questions
- Should login validation show distinct inline errors for "wrong password" vs. "unrecognized email," or a single generic error message? PO deferred this decision to spec review.
- No signup-screen design has been provided yet (only a "Sign up" link/stub on the login mock) — needed before signup fields/layout can be specified.
