"""core/git/diff.py — Git 分支差异分析"""
from __future__ import annotations

import re
import logging
from dataclasses import dataclass
from pathlib import Path

import git

log = logging.getLogger(__name__)


@dataclass
class DiffStat:
    files_changed: int
    added: int
    deleted: int
    base_branch: str
    target_branch: str

    @property
    def changed(self) -> int:
        return self.added + self.deleted


def _all_branch_names(repo: git.Repo) -> set[str]:
    """返回本地分支 + 所有远端分支名（去掉 origin/ 前缀）的集合。"""
    names: set[str] = {b.name for b in repo.branches}
    for remote in repo.remotes:
        for ref in remote.refs:
            names.add(ref.remote_head)
    return names


def resolve_base_branch(repo: git.Repo) -> str:
    """自动检测基准分支：优先 main，其次 master。"""
    existing = _all_branch_names(repo)
    for candidate in ("main", "master"):
        if candidate in existing:
            log.debug("自动检测基准分支: %s", candidate)
            return candidate
    raise ValueError("无法自动检测基准分支，请手动指定 --base")


_SHORTSTAT_RE = re.compile(
    r"(\d+) files? changed"
    r"(?:, (\d+) insertions?\(\+\))?"
    r"(?:, (\d+) deletions?\(-\))?"
)


def _parse_shortstat(output: str) -> tuple[int, int, int]:
    """解析 git diff --shortstat 输出，返回 (files_changed, added, deleted)。
    输出为空（两分支相同）时返回 (0, 0, 0)。
    """
    if not output.strip():
        return 0, 0, 0
    m = _SHORTSTAT_RE.search(output)
    if not m:
        return 0, 0, 0
    files = int(m.group(1))
    added = int(m.group(2) or 0)
    deleted = int(m.group(3) or 0)
    return files, added, deleted


def diff_stat(
    project_dir: Path,
    target_branch: str,
    base_branch: str | None = None,
) -> DiffStat:
    """计算两个分支间的代码差异汇总。

    Args:
        project_dir: Git 仓库根目录。
        target_branch: 待分析分支。
        base_branch: 基准分支；None 时自动检测 main/master。

    Returns:
        DiffStat 汇总数据。

    Raises:
        git.InvalidGitRepositoryError: project_dir 不是 Git 仓库。
        ValueError: 分支不存在或无法自动检测基准分支。
    """
    repo = git.Repo(project_dir)

    if base_branch is None:
        base_branch = resolve_base_branch(repo)

    existing = _all_branch_names(repo)
    if target_branch not in existing:
        raise ValueError(f"分支不存在: {target_branch}")

    log.debug("git diff --shortstat %s %s", base_branch, target_branch)
    raw = repo.git.diff("--shortstat", base_branch, target_branch)
    files_changed, added, deleted = _parse_shortstat(raw)

    return DiffStat(
        files_changed=files_changed,
        added=added,
        deleted=deleted,
        base_branch=base_branch,
        target_branch=target_branch,
    )
