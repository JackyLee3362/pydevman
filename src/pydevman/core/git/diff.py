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
