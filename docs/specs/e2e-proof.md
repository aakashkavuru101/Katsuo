# End-to-end proof

## Goal

Prove Katsuo from its package manifests through its Git guard, then provide one bounded command for live Claude Code and Codex behavior.

## Scope

**In:** package contracts, real hook wiring, host discovery, read-only live smoke tests, and clear evidence levels.

**Out:** adding a third-party runtime or claiming that model behavior is deterministic.

## Acceptance criteria

- **AC1:** Given the repository, when CI runs, then matching manifests, referenced files, and the packaged Git hook are verified.
- **AC2:** Given the packaged hook, when it receives real host-shaped input, then it blocks a protected-branch push and permits a feature-branch push.
- **AC3:** Given authenticated Claude Code and Codex installations, when the live smoke command runs, then both hosts invoke Katsuo read-only and classify a one-file typo fix as `Small`.
- **AC4:** The proof stores no credentials, disables Claude tools, confines Codex to a read-only sandbox, and reports failures without claiming success.

## Task graph

| ID | Task | Depends on | Covers | Status |
|---|---|---|---|---|
| T1 | Add package and hook-wiring tests | - | AC1, AC2 | done |
| T2 | Add the bounded host smoke command | T1 | AC3, AC4 | done |
| T3 | Document evidence and commands | T2 | AC1-AC4 | done |
