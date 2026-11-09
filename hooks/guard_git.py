#!/usr/bin/env python3
"""katsuo PreToolUse hook: keep the agent on a PR-only, spec-driven workflow in GitHub repos.

Blocks (exit 2):
  - pushes to protected branches, force/bulk pushes, `gh pr merge`,
    and commits made directly on a protected branch;
  - commits or pushes that introduce high-confidence secrets;
  - pushes from a `feat/<slug>` branch that has no `docs/specs/<slug>.md`.

The user can still do any of these themselves in their own terminal.
Any error inside the hook allows the command (exit 0) so it never breaks a session.
"""
import json
import os
import re
import shlex
import subprocess
import sys

PROTECTED = {"main", "master"}
SEPARATORS = {"&&", "||", ";", "|", "&", ";;"}
GIT_OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}

# High-confidence, low false-positive secret patterns. Match only; never print the value.
SECRET_PATTERNS = [
    ("private key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("OpenAI key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
]


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


def scan_for_secrets(diff):
    findings = []
    for line in diff.splitlines():
        if not (line.startswith("+") and not line.startswith("+++")):
            continue
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append(name)
                break
    return findings


def secret_message(findings, action):
    kinds = ", ".join(sorted(set(findings)))
    return f"{action} contains potential secrets ({kinds}); remove them before proceeding"


def check_spec(current, cwd):
    if not current.startswith("feat/"):
        return None
    slug = current[len("feat/"):].strip()
    if not slug:
        return None
    if os.path.isfile(os.path.join(cwd, "docs", "specs", f"{slug}.md")):
        return None
    return (f"no spec at docs/specs/{slug}.md for branch '{current}'; "
            "write the spec before pushing")


def check_staged_secrets(cwd):
    findings = scan_for_secrets(sh(cwd, "git", "diff", "--cached", "--unified=0"))
    return secret_message(findings, "commit") if findings else None


def check_push_secrets(current, cwd):
    base = ""
    for upstream in ("origin/main", "main", "origin/master", "master"):
        base = sh(cwd, "git", "merge-base", upstream, current)
        if base:
            break
    if not base:
        return None  # cannot determine the base; fail open
    findings = scan_for_secrets(sh(cwd, "git", "diff", f"{base}...{current}", "--unified=0"))
    return secret_message(findings, "push") if findings else None


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
            reason = check_spec(current, cwd)
            if reason:
                return reason
            reason = check_push_secrets(current, cwd)
            if reason:
                return reason
        if sub == "commit":
            if current in PROTECTED:
                return f"committing directly on '{current}' is not allowed; create a branch first (git switch -c feat/<name>)"
            reason = check_staged_secrets(cwd)
            if reason:
                return reason
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
