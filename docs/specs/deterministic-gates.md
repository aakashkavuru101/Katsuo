# Deterministic quality gates

## Goal

Enforce Katsuo's spec-driven and privacy-first contracts with hooks, not just prompts.

## Scope

**In:** a secret guard (commit + push) and a spec guard (push) in `hooks/guard_git.py`, with tests.

**Out:** full secret scanning beyond high-confidence patterns, and replacing human judgement.

## Acceptance criteria

- **AC1:** Given a staged change that introduces a known secret, when the agent commits, then the hook blocks the commit.
- **AC2:** Given a `feat/<slug>` branch with no `docs/specs/<slug>.md`, when the agent pushes, then the hook blocks the push.
- **AC3:** Given a feature branch with a spec and no secrets, when the agent pushes, then the hook allows it.
- **AC4:** Any error inside the hook still allows the command, so a session is never broken.

## Task graph

| ID | Task | Depends on | Covers | Status |
|---|---|---|---|---|
| T1 | Add secret patterns and a diff scanner | - | AC1 | done |
| T2 | Add the spec gate on push | T1 | AC2, AC3 | done |
| T3 | Add tests and document the gates | T2 | AC1-AC4 | done |
