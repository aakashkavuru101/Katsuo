"""Tests for hooks/guard_git.py. Run: python3 -m unittest discover tests"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HOOK = os.path.join(os.path.dirname(__file__), "..", "hooks", "guard_git.py")


def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def make_repo(remote="https://github.com/acme/app.git", branch="main"):
    d = tempfile.mkdtemp()
    git(d, "init", "-q", "-b", "main")
    git(d, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "init")
    if remote:
        git(d, "remote", "add", "origin", remote)
    if branch != "main":
        git(d, "switch", "-q", "-c", branch)
    return d


def write_spec(repo, slug):
    d = os.path.join(repo, "docs", "specs")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, f"{slug}.md"), "w") as f:
        f.write("# spec\n")


def run_hook(command, cwd):
    payload = {"tool_name": "Bash", "tool_input": {"command": command}, "cwd": cwd}
    return subprocess.run([sys.executable, HOOK], input=json.dumps(payload),
                          capture_output=True, text=True, cwd=cwd)


class GuardGitTest(unittest.TestCase):
    def assertBlocked(self, command, **repo):
        r = run_hook(command, make_repo(**repo))
        self.assertEqual(r.returncode, 2, f"expected block: {command}")
        self.assertIn("Blocked by katsuo", r.stderr)

    def assertAllowed(self, command, **repo):
        r = run_hook(command, make_repo(**repo))
        self.assertEqual(r.returncode, 0, f"expected allow: {command}\n{r.stderr}")

    # --- pushes to protected branches are blocked
    def test_push_explicit_main(self):
        self.assertBlocked("git push origin main", branch="feat/x")

    def test_push_refspec_to_main(self):
        self.assertBlocked("git push origin feat/x:main", branch="feat/x")

    def test_push_while_on_main(self):
        self.assertBlocked("git push")

    def test_push_head_while_on_master(self):
        self.assertBlocked("git push -u origin HEAD", branch="master")

    def test_delete_remote_main(self):
        self.assertBlocked("git push origin --delete main", branch="feat/x")

    def test_push_inside_chain(self):
        self.assertBlocked("npm test && git push origin main", branch="feat/x")

    def test_push_with_global_option(self):
        self.assertBlocked("git -C . push origin main", branch="feat/x")

    # --- force and bulk pushes are blocked everywhere
    def test_force_flag(self):
        self.assertBlocked("git push --force origin feat/x", branch="feat/x")

    def test_force_short_cluster(self):
        self.assertBlocked("git push -fu origin feat/x", branch="feat/x")

    def test_force_with_lease(self):
        self.assertBlocked("git push --force-with-lease origin feat/x", branch="feat/x")

    def test_plus_refspec(self):
        self.assertBlocked("git push origin +feat/x", branch="feat/x")

    def test_push_all(self):
        self.assertBlocked("git push --all origin", branch="feat/x")

    # --- merging and committing on protected branches are blocked
    def test_gh_pr_merge(self):
        self.assertBlocked("gh pr merge 12 --squash", branch="feat/x")

    def test_commit_on_main(self):
        self.assertBlocked("git commit -m 'wip'")

    # --- normal PR workflow is allowed (a spec must exist first)
    def test_push_feature_branch(self):
        repo = make_repo(branch="feat/x")
        write_spec(repo, "x")
        self.assertEqual(run_hook("git push -u origin feat/x", repo).returncode, 0)

    def test_push_feature_branch_implicit(self):
        repo = make_repo(branch="feat/x")
        write_spec(repo, "x")
        self.assertEqual(run_hook("git push", repo).returncode, 0)

    def test_commit_on_feature(self):
        self.assertAllowed("git commit -m 'feat: x'", branch="feat/x")

    def test_gh_pr_create(self):
        self.assertAllowed("gh pr create --fill", branch="feat/x")

    def test_unrelated_command(self):
        self.assertAllowed("echo 'git push origin main is blocked'")

    # --- secrets are blocked at commit and push
    def test_commit_with_secret(self):
        repo = make_repo(branch="feat/x")
        with open(os.path.join(repo, "leak.txt"), "w") as f:
            f.write("token = ghp_12345678901234567890\n")
        git(repo, "add", "leak.txt")
        r = run_hook("git commit -m 'x'", repo)
        self.assertEqual(r.returncode, 2, "expected secret block")
        self.assertIn("potential secrets", r.stderr)

    def test_commit_without_secret(self):
        repo = make_repo(branch="feat/x")
        with open(os.path.join(repo, "ok.txt"), "w") as f:
            f.write("hello world\n")
        git(repo, "add", "ok.txt")
        self.assertEqual(run_hook("git commit -m 'x'", repo).returncode, 0)

    def test_push_with_secret(self):
        repo = make_repo(branch="feat/x")
        write_spec(repo, "x")
        git(repo, "add", "docs")
        git(repo, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "spec")
        with open(os.path.join(repo, "leak.txt"), "w") as f:
            f.write("AKIAIOSFODNN7EXAMPLE\n")
        git(repo, "add", "leak.txt")
        git(repo, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "leak")
        r = run_hook("git push -u origin feat/x", repo)
        self.assertEqual(r.returncode, 2, "expected secret block on push")
        self.assertIn("potential secrets", r.stderr)

    # --- spec gate on push
    def test_push_feat_without_spec(self):
        repo = make_repo(branch="feat/x")
        r = run_hook("git push -u origin feat/x", repo)
        self.assertEqual(r.returncode, 2, "expected spec block")
        self.assertIn("no spec", r.stderr)

    def test_push_feat_with_spec(self):
        repo = make_repo(branch="feat/x")
        write_spec(repo, "x")
        git(repo, "add", "docs")
        git(repo, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "spec")
        self.assertEqual(run_hook("git push -u origin feat/x", repo).returncode, 0)

    def test_push_non_feat_without_spec(self):
        repo = make_repo(branch="fix/x")
        self.assertEqual(run_hook("git push -u origin fix/x", repo).returncode, 0)

    # --- rule only applies to GitHub repos
    def test_non_github_remote(self):
        self.assertAllowed("git push origin main", remote="https://gitlab.com/acme/app.git")

    def test_no_remote(self):
        self.assertAllowed("git commit -m x", remote=None)

    def test_not_a_repo(self):
        d = tempfile.mkdtemp()
        self.assertEqual(run_hook("git push origin main", d).returncode, 0)

    def test_bad_input_never_crashes(self):
        r = subprocess.run([sys.executable, HOOK], input="not json", capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
