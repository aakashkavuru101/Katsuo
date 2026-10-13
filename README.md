# katsuo

[![Tests](https://github.com/AllBlue-inc/Katsuo/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/AllBlue-inc/Katsuo/actions/workflows/test.yml)

**English** | [日本語](README_JA.md)

A development plugin for Claude Code and Codex. It leads with the answer, keeps steps short, and leaves tangents out. It works in this order: spec → test-driven build → independent review → Pull Request.

## Install

**Claude Code**

```bash
claude plugin marketplace add AllBlue-inc/katsuo && claude plugin install katsuo@katsuo
```

**Codex**

```bash
codex plugin marketplace add AllBlue-inc/katsuo && codex plugin add katsuo@katsuo
```

In Codex, open `/hooks` after installing and trust Katsuo's hook.

The hook needs `python3` on `PATH`. The `gh` CLI is recommended for Pull Requests.

**Update:** `claude plugin marketplace update katsuo` · **Remove:** `claude plugin uninstall katsuo@katsuo` / `codex plugin remove katsuo`

## Usage

Type `/katsuo` in Claude Code, or `$katsuo` in Codex, followed by what you want to build.

```text
/katsuo add password reset by email
```

1. Katsuo classifies the change as small or big and proposes the first function to build. Agree on the scope.
2. First run only: it asks about the project (up to 3 questions at a time). Your answers create `docs/project.md` and `AGENTS.md`.
3. Approve the acceptance criteria and task list (`docs/specs/<name>.md`).
4. Katsuo writes a test before the code for each task. After 3 failed attempts on a task, it asks you.
5. A read-only reviewer checks the diff, and any problems are fixed.
6. You get a Pull Request link. You merge it.

A hook blocks the agent from pushing to `main`/`master`, force-pushing, or merging.

## For developers

### Tests

```bash
python3 tests/e2e_smoke.py          # check the package and hook wiring
python3 tests/e2e_smoke.py --live   # run Katsuo in authenticated Claude Code and Codex
```

### Files

```text
skills/katsuo/SKILL.md  the command and working process
agents/reviewer.md      independent reviewer (read-only)
hooks/guard_git.py      Git guard
tests/e2e_smoke.py      deterministic and live tests
```

Author: Aakash
