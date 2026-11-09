#!/usr/bin/env python3
"""Run deterministic checks; add --live for bounded Claude Code and Codex smokes."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROMPT = (
    "Use the Katsuo skill. This is a read-only smoke test: do not use tools or change files. "
    "The proposed work is to fix one typo in README.md. Reply with the size classification "
    "Small or Big, followed by one sentence explaining why."
)


def run(label, command, timeout=120):
    print(f"RUN  {label}")
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        raise RuntimeError(f"{label}: {detail}")
    print(f"PASS {label}")
    return result.stdout


def live(label, command, parser, timeout):
    try:
        assert_small(label, parser(run(f"{label} live smoke", command, timeout)))
        return None
    except (json.JSONDecodeError, RuntimeError, subprocess.TimeoutExpired) as error:
        return f"{label}: {error}"


def claude_result(output):
    value = json.loads(output)
    return value.get("result", "")


def codex_result(output):
    messages = []
    for line in output.splitlines():
        event = json.loads(line)
        item = event.get("item", {})
        if event.get("type") == "item.completed" and item.get("type") == "agent_message":
            messages.append(item.get("text", ""))
    return "\n".join(messages)


def assert_small(label, text):
    first = text.lstrip(" \n#*`").split(maxsplit=1)
    if not first or first[0].rstrip(":*`.,—-").lower() != "small":
        raise RuntimeError(f"{label}: response did not classify the change as Small")
    if len(text.split()) > 40:
        raise RuntimeError(f"{label}: response buried the answer in more than 40 words")
    print(f"PASS {label} behavior")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="invoke both authenticated hosts read-only")
    parser.add_argument("--timeout", type=int, default=120, help="seconds allowed for each live host")
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("--timeout must be at least 1")

    run("test suite", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])

    if shutil.which("claude"):
        run("Claude package validation", ["claude", "plugin", "validate", "."])
    else:
        print("SKIP Claude package validation (claude is not installed)")

    if shutil.which("codex"):
        plugins = run("Codex plugin discovery", ["codex", "plugin", "list"])
        if "katsuo@katsuo" not in plugins or "installed, enabled" not in plugins:
            raise RuntimeError("Codex plugin discovery: katsuo is not installed and enabled")
    else:
        print("SKIP Codex plugin discovery (codex is not installed)")

    if not args.live:
        print("PASS deterministic proof; use --live for authenticated host behavior")
        return

    failures = []
    if shutil.which("claude"):
        failure = live(
            "Claude",
            [
                "claude", "--plugin-dir", str(ROOT), "--print", "--no-session-persistence",
                "--max-turns", "1", "--tools", "", "--permission-prompts", "none",
                "--output-format", "json", f"/katsuo {PROMPT}",
            ],
            claude_result,
            args.timeout,
        )
        if failure:
            failures.append(failure)
    else:
        failures.append("Claude: claude is not installed")

    if shutil.which("codex"):
        failure = live(
            "Codex",
            [
                "codex", "exec", "--ephemeral", "--skip-git-repo-check", "--sandbox", "read-only",
                "--json", f"$katsuo {PROMPT}",
            ],
            codex_result,
            args.timeout,
        )
        if failure:
            failures.append(failure)
    else:
        failures.append("Codex: codex is not installed")
    if failures:
        raise RuntimeError("live proof failed:\n- " + "\n- ".join(failures))
    print("PASS live end-to-end proof")


if __name__ == "__main__":
    try:
        main()
    except (json.JSONDecodeError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(f"FAIL {error}", file=sys.stderr)
        sys.exit(1)
