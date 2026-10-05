# katsuo 🐟

[![Tests](https://github.com/AllBlue-inc/Katsuo/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/AllBlue-inc/Katsuo/actions/workflows/test.yml)
![Version](https://img.shields.io/badge/version-0.1.0-2563eb)
![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-d97757)
![Codex](https://img.shields.io/badge/Codex-plugin-111827)

**English** | [日本語](README_JA.md)

Your curious AI development partner.
Like dashi from katsuobushi: one ingredient, full flavour.

```text
/katsuo add password reset by email
```

Spec → test-driven build → independent review → Pull Request. That's it.

## The idea

Katsuo is a curious fish. It gathers the facts before it acts and makes decisions with you, not for you. When a decision needs your input, Katsuo asks. When you are unsure, it researches the options and explains its recommendation in plain language.

You and Katsuo are a team. Privacy and security come first. Every change follows a visible process, adapts to the project, and stays as small as it can be while still working well. Katsuo is designed for everyone; you do not need to know the technical words to use it.

## Principles

- **Curious:** inspect the project and gather evidence before deciding.
- **Together:** involve you in decisions that change the outcome or risk.
- **Clear:** explain unfamiliar ideas in simple language.
- **Private and secure:** protect data, secrets, access, and user control by default.
- **Structured:** follow a clear spec → build → review → PR process.
- **Minimal and functional:** build the smallest solution that fully works.
- **Adaptive:** fit the project's tools, environment, and the user's experience.

## What it does

| Step | What happens | You decide |
|---|---|---|
| Setup (first run) | Learns the project, asks a few questions, and sets proportionate guardrails | Confirm the decisions |
| Spec | Writes acceptance criteria and a task graph | Approve the plan |
| Build | Works red → green → refactor per task, with a three-attempt limit | Approve per task or feature |
| Review | Uses a fresh read-only reviewer for the spec, tests, security, and simplicity | Resolve any remaining blockers |
| PR | Pushes a feature branch and opens a Pull Request | You merge |

The agent cannot push to `main`/`master`, force-push, or merge in GitHub repositories. A hook blocks it. You still can.

## Install

**Claude Code**

```bash
claude plugin marketplace add AllBlue-inc/katsuo && claude plugin install katsuo@katsuo
```

**Codex**

```bash
codex plugin marketplace add AllBlue-inc/katsuo && codex plugin add katsuo@katsuo
```

Then open `/hooks` in Codex and trust Katsuo's hook.

Run it with `/katsuo` in Claude Code, or `$katsuo` in Codex.

Katsuo needs `python3` on `PATH` for the hook. The `gh` CLI is recommended for Pull Requests.

**Update:** `claude plugin marketplace update katsuo` · **Remove:** `claude plugin uninstall katsuo@katsuo` / `codex plugin remove katsuo`

## Files

```text
skills/katsuo/SKILL.md  the command and working process
agents/reviewer.md      independent reviewer (read-only)
hooks/guard_git.py      PR-only Git guard
```

Author: Aakash
