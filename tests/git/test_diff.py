from pathlib import Path

import git
from pydevman.core.git.diff import DiffStat, resolve_base_branch

# 以 pydevman 仓库自身作为测试 fixture
REPO_ROOT = Path(__file__).parent.parent.parent


def test_diff_stat_dataclass():
    stat = DiffStat(
        files_changed=3,
        added=42,
        deleted=7,
        base_branch="main",
        target_branch="feature",
    )
    assert stat.files_changed == 3
    assert stat.added == 42
    assert stat.deleted == 7
    assert stat.changed == 49          # added + deleted
    assert stat.base_branch == "main"
    assert stat.target_branch == "feature"


def test_resolve_base_branch_returns_main():
    repo = git.Repo(REPO_ROOT)
    branch = resolve_base_branch(repo)
    assert branch == "main"
