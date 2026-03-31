import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "git-union"


def run(cmd, cwd=None, env=None, check=True):
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        check=check,
        text=True,
        capture_output=True,
    )


def git(cwd: Path, *args, check=True):
    return run(["git", *args], cwd=cwd, check=check)


class GitUnionTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="git-union-tests-"))
        self.repo1 = self.tmpdir / "repo1"
        self.repo2 = self.tmpdir / "repo2"
        self.repo1.mkdir()
        self.repo2.mkdir()
        git(self.repo1, "init")
        git(self.repo2, "init")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _commit(self, repo: Path, path: str, content: str, msg: str, when_iso: str):
        f = repo / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content, encoding="utf-8")
        git(repo, "add", path)
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = when_iso
        env["GIT_COMMITTER_DATE"] = when_iso
        run(
            [
                "git",
                "-c",
                "user.name=Test User",
                "-c",
                "user.email=test@example.com",
                "commit",
                "-m",
                msg,
            ],
            cwd=repo,
            env=env,
        )

    def _union(self, *args):
        return run([str(SCRIPT), *args])

    def test_basic_union_creates_subdirs_and_commits(self):
        self._commit(self.repo1, "a.txt", "a1\n", "r1-c1", "2020-01-01T00:00:10Z")
        self._commit(self.repo2, "b.txt", "b1\n", "r2-c1", "2020-01-01T00:00:08Z")

        mono = self.tmpdir / "mono"
        self._union(str(mono), str(self.repo1), str(self.repo2))

        self.assertTrue((mono / "repo1" / "a.txt").exists())
        self.assertTrue((mono / "repo2" / "b.txt").exists())
        log = git(mono, "log", "--reverse", "--pretty=%s").stdout.strip().splitlines()
        self.assertEqual(log, ["r1-c1", "r2-c1"])

    def test_sort_respects_per_repo_order(self):
        self._commit(self.repo1, "f.txt", "1\n", "r1-10", "2020-01-01T00:00:10Z")
        self._commit(self.repo1, "f.txt", "2\n", "r1-45", "2020-01-01T00:00:45Z")
        self._commit(self.repo1, "f.txt", "3\n", "r1-33", "2020-01-01T00:00:33Z")
        self._commit(self.repo2, "g.txt", "1\n", "r2-08", "2020-01-01T00:00:08Z")
        self._commit(self.repo2, "g.txt", "2\n", "r2-13", "2020-01-01T00:00:13Z")
        self._commit(self.repo2, "g.txt", "3\n", "r2-31", "2020-01-01T00:00:31Z")

        mono = self.tmpdir / "mono-sorted"
        self._union("--sort", str(mono), str(self.repo1), str(self.repo2))

        log = git(mono, "log", "--reverse", "--pretty=%s").stdout.strip().splitlines()
        # Key rule: repo1 order stays r1-10 -> r1-45 -> r1-33.
        self.assertLess(log.index("r1-10"), log.index("r1-45"))
        self.assertLess(log.index("r1-45"), log.index("r1-33"))
        # Same for repo2 order.
        self.assertLess(log.index("r2-08"), log.index("r2-13"))
        self.assertLess(log.index("r2-13"), log.index("r2-31"))

    def test_explicit_name_mapping(self):
        self._commit(self.repo1, "x.txt", "x\n", "c1", "2020-01-01T00:00:00Z")
        mono = self.tmpdir / "mono-map"
        self._union(str(mono), f"alpha={self.repo1}")
        self.assertTrue((mono / "alpha" / "x.txt").exists())
        self.assertFalse((mono / "repo1").exists())


if __name__ == "__main__":
    unittest.main()
