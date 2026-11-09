# katsuo 🐟

[![Tests](https://github.com/aakashkavuru101/Katsuo/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/aakashkavuru101/Katsuo/actions/workflows/test.yml)
![Live E2E](https://img.shields.io/badge/live%20E2E-Claude%20Code%20%2B%20Codex%20passed-2ea44f)
![Version](https://img.shields.io/badge/version-0.3.0-2563eb)
![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-d97757)
![Codex](https://img.shields.io/badge/Codex-plugin-111827)

**English** | [日本語](README_JA.md)

Your curious AI development partner.
Like dashi from katsuobushi: one ingredient, full flavour.

```text
/katsuo add password reset by email
```

Spec → test-driven build → independent review → Pull Request, then it learns for next time. That's it.

## The idea

Katsuo is a curious fish. It gathers the facts before it acts and makes decisions with you, not for you. When a decision needs your input, Katsuo asks. When you are unsure, it researches the options and explains its recommendation in plain language.

You and Katsuo are a team. Privacy and security come first. Katsuo decides with you whether a change is small or big, then completes one useful function at a time instead of attempting the whole picture in one go. Every change follows a visible process, adapts to the project, and stays as small as it can be while still working well. Katsuo is designed for everyone; you do not need to know the technical words to use it. Katsuo also remembers what it learns, so it gets a little better every day you use it.

## Principles

- **Curious:** inspect the project and gather evidence before deciding.
- **Together:** involve you in decisions that change the outcome or risk.
- **Clear:** explain unfamiliar ideas in simple language.
- **Private and secure:** protect data, secrets, access, and user control by default.
- **Structured:** follow a clear spec → build → review → PR process.
- **Right-sized:** identify whether the change is small or big, explain why, and agree on the first useful slice with you.
- **Function by function:** complete one useful capability before moving to the next.
- **Minimal and functional:** build the smallest solution that fully works.
- **Adaptive:** fit the project's tools, environment, and the user's experience.
- **Improves every day:** remember each project's lessons and decisions and apply them on the next run.

## What it does

| Step | What happens | You decide |
|---|---|---|
| Scope | Classifies the change as small or big and proposes the smallest useful function | Agree on the scope |
| Setup (first run) | Learns the project, asks a few questions, and sets proportionate guardrails | Confirm the decisions |
| Spec | Writes acceptance criteria and a task graph | Approve the plan |
| Build | Works red → green → refactor per task, with a three-attempt limit | Approve per task or feature |
| Review | Uses a fresh read-only reviewer for the spec, tests, security, and simplicity | Resolve any remaining blockers |
| PR | Pushes a feature branch and opens a Pull Request | You merge |
| Learn | Looks back and records durable lessons into project memory, so the next run starts smarter | What to remember |

Hard guards — enforced by a hook, not just instructions:

- No push to `main`/`master`, no force-push, and no `gh pr merge`.
- No commit or push that introduces a secret (keys and tokens are matched).
- No push from a `feat/<slug>` branch without `docs/specs/<slug>.md`.

The agent cannot do any of these; a hook blocks it. You still can.

## Install

**Claude Code**

```bash
claude plugin marketplace add aakashkavuru101/katsuo && claude plugin install katsuo@katsuo
```

**Codex**

```bash
codex plugin marketplace add aakashkavuru101/katsuo && codex plugin add katsuo@katsuo
```

Then open `/hooks` in Codex and trust Katsuo's hook.

Run it with `/katsuo` in Claude Code, or `$katsuo` in Codex.

Katsuo needs `python3` on `PATH` for the hook. The `gh` CLI is recommended for Pull Requests.

**Update:** `claude plugin marketplace update katsuo` · **Remove:** `claude plugin uninstall katsuo@katsuo` / `codex plugin remove katsuo`

## Proof

```bash
python3 tests/e2e_smoke.py
python3 tests/e2e_smoke.py --live
```

The first command proves the package contracts and the real manifest-to-hook path, validates the Claude package when Claude Code is installed, and confirms Codex discovery when Codex is installed. `--live` also invokes Katsuo through both authenticated hosts and checks its response. Claude tools are disabled and Codex runs in its read-only sandbox. Credentials stay with the host CLIs and are never stored by the test.

**Verified 2026-10-06:** the deterministic suite, Claude Code live smoke, and Codex live smoke all passed.

| Evidence | What it proves |
|---|---|
| CI test suite | Package consistency, referenced files, guard behavior, and packaged hook wiring |
| Claude validation | Claude Code accepts the plugin package |
| Codex discovery | Codex has Katsuo installed and enabled |
| Live smoke | Passed: both hosts loaded and ran Katsuo's skill |

A passing test proves the tested path. It does not make every future model decision deterministic.

## Files

```text
skills/katsuo/SKILL.md  the command and working process
agents/reviewer.md      independent reviewer (read-only)
hooks/guard_git.py      PR-only Git guard
tests/e2e_smoke.py      deterministic and live proof command
CHANGELOG.md            what changed in each release
LICENSE                 MIT
```

Author: Aakash
