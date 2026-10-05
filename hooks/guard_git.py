#!/usr/bin/env python3
"""katsuo PreToolUse hook: keep the agent on a PR-only workflow in GitHub repos.

Blocks (exit 2): pushes to protected branches, force/bulk pushes,
`gh pr merge`, and commits made directly on a protected branch.
The user can still do any of these themselves in their own terminal.
Any error inside the hook allows the command (exit 0) so it never breaks a session.
"""
import json
import shlex
import subprocess
import sys

PROTECTED = {"main", "master"}
SEPARATORS = {"&&", "||", ";", "|", "&", ";;"}
GIT_OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}


def sh(cwd, *args):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=5)
    return r.stdout.strip() if r.returncode == 0 else ""


def segments(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    seg = []
    for tok in lexer:
        if tok in SEPARATORS:
            if seg:
                yield seg
            seg = []
        else:
            seg.append(tok)
    if seg:
        yield seg


def git_subcommand(tokens):
    """['git', '-C', '.', 'push', ...] -> ('push', [...rest])"""
    i = 1
    while i < len(tokens) and tokens[i].startswith("-"):
        i += 2 if tokens[i] in GIT_OPTS_WITH_VALUE else 1
    return (tokens[i], tokens[i + 1:]) if i < len(tokens) else (None, [])


def check_push(args, current):
    positional = []
    skip = False
    for a in args:
        if skip:
            skip = False
            continue
        if a in ("-o", "--push-option", "--repo"):
            skip = True
        elif a.startswith("--force") or (a.startswith("-") and not a.startswith("--") and "f" in a):
            return "force pushes are not allowed"
        elif a in ("--all", "--mirror"):
            return "bulk pushes (--all/--mirror) are not allowed"
        elif not a.startswith("-"):
            positional.append(a)

    refspecs = positional[1:] or [current]
    for spec in refspecs:
        if spec.startswith("+"):
            return "force pushes are not allowed"
        dst = spec.split(":")[-1].replace("refs/heads/", "")
        if dst == "HEAD":
            dst = current
        if dst in PROTECTED:
            return f"pushing to '{dst}' is not allowed"
    return None


def violation(command, cwd):
    if not any(t in command for t in ("git", "gh")):
        return None
    if "github" not in sh(cwd, "git", "remote", "-v"):
        return None  # rule applies to GitHub repos only
    current = sh(cwd, "git", "rev-parse", "--abbrev-ref", "HEAD")

    for tokens in segments(command):
        if tokens[:3] == ["gh", "pr", "merge"]:
            return "merging PRs is the user's decision"
        if tokens[0] != "git":
            continue
        sub, rest = git_subcommand(tokens)
        if sub == "push":
            reason = check_push(rest, current)
            if reason:
                return reason
        if sub == "commit" and current in PROTECTED:
            return f"committing directly on '{current}' is not allowed; create a branch first (git switch -c feat/<name>)"
    return None


def main():
    try:
        data = json.load(sys.stdin)
        command = data.get("tool_input", {}).get("command", "")
        reason = violation(command, data.get("cwd") or None)
    except Exception:
        return 0
    if reason:
        print(f"Blocked by katsuo: {reason}. Push a feature branch and open a Pull Request instead. "
              "The user can run this command manually if they really intend it.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
