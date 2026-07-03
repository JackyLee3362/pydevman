from pathlib import Path

import git
from pydevman.core.git.diff import DiffStat, _parse_shortstat, diff_stat, resolve_base_branch

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


def test_diff_stat_same_branch_returns_zeros():
    """同分支对比，所有数值为 0。"""
    result = diff_stat(REPO_ROOT, "main", base_branch="main")
    assert result.files_changed == 0
    assert result.added == 0
    assert result.deleted == 0
    assert result.changed == 0
    assert result.base_branch == "main"
    assert result.target_branch == "main"


def test_diff_stat_auto_detect_base_branch():
    """不传 base_branch 时自动检测为 main。"""
    result = diff_stat(REPO_ROOT, "main")
    assert result.base_branch == "main"


def test_diff_stat_invalid_repo_raises():
    import tempfile
    import pytest
    with tempfile.TemporaryDirectory() as tmp:
        with pytest.raises(git.InvalidGitRepositoryError):
            diff_stat(Path(tmp), "main")


def test_diff_stat_invalid_branch_raises():
    import pytest
    with pytest.raises(ValueError, match="分支不存在"):
        diff_stat(REPO_ROOT, "branch-that-does-not-exist-xyz")


def test_parse_shortstat_empty():
    assert _parse_shortstat("") == (0, 0, 0)


def test_parse_shortstat_insertions_only():
    assert _parse_shortstat(" 1 file changed, 5 insertions(+)") == (1, 5, 0)


def test_parse_shortstat_deletions_only():
    assert _parse_shortstat(" 1 file changed, 3 deletions(-)") == (1, 0, 3)


def test_parse_shortstat_both():
    assert _parse_shortstat(" 3 files changed, 42 insertions(+), 7 deletions(-)") == (3, 42, 7)
