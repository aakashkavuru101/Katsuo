# katsuo 🐟

One command for AI-driven development.
Like dashi from katsuobushi: one ingredient, full flavour.

```
/katsuo add password reset by email
```

Spec → test-driven build → independent review → Pull Request. That's it.

## What it does

| Step | What happens | You decide |
|---|---|---|
| Setup (first run) | Asks a few questions, sets guardrails, containers, rate limits, memory | Confirm decisions |
| Spec | Acceptance criteria + task graph | Approve |
| Build | Red → green → refactor per task, max 3 attempts | Per task or per feature |
| Review | Fresh read-only reviewer: spec, tests, security, simplicity | Only if blockers remain |
| PR | Pushes a feature branch, opens a PR | You merge |

The agent can't push to `main`/`master`, force-push, or merge in GitHub repos. A hook blocks it. You still can.

## Install

**Claude Code**

```bash
claude plugin marketplace add AllBlue-inc/katsuo && claude plugin install katsuo@katsuo
```

**Codex**

```bash
codex plugin marketplace add AllBlue-inc/katsuo && codex plugin add katsuo@katsuo
```

Then open `/hooks` in Codex and trust katsuo's hook.

Run it with `/katsuo` in Claude Code, or `$katsuo` in Codex.

Needs `python3` on PATH for the hook. `gh` CLI recommended for PRs.

**Update:** `claude plugin marketplace update katsuo` · **Remove:** `claude plugin uninstall katsuo@katsuo` / `codex plugin remove katsuo`

## Files

```
skills/katsuo/SKILL.md   the command
agents/reviewer.md     independent reviewer (read-only)
hooks/guard_git.py     PR-only guard
```

Author: Aakash
