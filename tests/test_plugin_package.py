"""Package contracts and the manifest-to-hook path."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


def make_repo(branch):
    path = tempfile.mkdtemp()
    subprocess.run(["git", "init", "-q", "-b", branch], cwd=path, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "init"],
        cwd=path,
        check=True,
    )
    subprocess.run(
        ["git", "remote", "add", "origin", "https://github.com/acme/app.git"],
        cwd=path,
        check=True,
    )
    return path


class PluginPackageTest(unittest.TestCase):
    def test_manifests_describe_the_same_plugin(self):
        manifests = [load("plugin.json"), load(".claude-plugin/plugin.json")]
        self.assertEqual({m["name"] for m in manifests}, {"katsuo"})
        self.assertEqual(len({m["version"] for m in manifests}), 1)
        self.assertEqual(load(".claude-plugin/marketplace.json")["plugins"][0]["source"], "./")
        self.assertEqual(load(".agents/plugins/marketplace.json")["plugins"][0]["source"]["path"], "./")

    def test_package_references_exist(self):
        for path in ("skills/katsuo/SKILL.md", "agents/reviewer.md", "hooks/guard_git.py"):
            self.assertTrue((ROOT / path).is_file(), path)
        self.assertTrue(os.access(ROOT / "hooks/guard_git.py", os.X_OK))

    def test_learning_loop_and_license_present(self):
        skill = (ROOT / "skills/katsuo/SKILL.md").read_text()
        self.assertIn("## Start from memory", skill)
        self.assertIn("## 5. Learn", skill)
        self.assertTrue((ROOT / "LICENSE").is_file())
        self.assertTrue((ROOT / "CHANGELOG.md").is_file())

    def test_packaged_hook_blocks_main_and_allows_feature(self):
        hook = load("hooks/hooks.json")["hooks"]["PreToolUse"][0]["hooks"][0]
        command = hook["command"].replace("${CLAUDE_PLUGIN_ROOT}", str(ROOT))
        argv = shlex.split(command)

        def invoke(shell_command, branch):
            cwd = make_repo(branch)
            payload = {"tool_name": "Bash", "tool_input": {"command": shell_command}, "cwd": cwd}
            return subprocess.run(argv, input=json.dumps(payload), text=True, capture_output=True, cwd=cwd)

        blocked = invoke("git push origin main", "main")
        allowed = invoke("git push -u origin feat/e2e", "feat/e2e")
        self.assertEqual(blocked.returncode, 2, blocked.stderr)
        self.assertIn("Blocked by katsuo", blocked.stderr)
        self.assertEqual(allowed.returncode, 0, allowed.stderr)


if __name__ == "__main__":
    unittest.main()
