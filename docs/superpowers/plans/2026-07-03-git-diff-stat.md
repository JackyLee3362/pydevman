# git diff-stat 模块 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 新增 `core/git` 模块，通过 GitPython 分析两分支间的代码差异，输出汇总报告（新增/删除/变更行数），并提供 `pydevman git diff-stat` CLI 命令。

**Architecture:** 核心逻辑放在 `core/git/diff.py`，返回 `DiffStat` dataclass；CLI 层 `cli/git_cmd.py` 调用核心函数并用 `rich` 表格渲染；注册到 `__main__.py` 的 `git` 子命令组。

**Tech Stack:** `gitpython>=3.1`、`typer`、`rich`、`dataclasses`、`re`

## Global Constraints

- Python >= 3.14（`pyproject.toml` 已声明）
- 使用 `uv` 管理依赖，安装命令：`uv sync`
- 测试框架：`pytest`，运行命令：`uv run pytest tests/git/ -v`
- 代码风格：跟随 `core/file/stat.py` — logging 用 `logging`，无 type alias
- 分支自动检测优先级：`main` → `master`

---

## 文件结构

| 文件 | 操作 | 职责 |
|---|---|---|
| `pyproject.toml` | 修改 | 新增 `gitpython>=3.1` 依赖 |
| `src/pydevman/core/git/__init__.py` | 新建 | 空文件，声明包 |
| `src/pydevman/core/git/diff.py` | 新建 | `DiffStat`、`resolve_base_branch`、`diff_stat` |
| `src/pydevman/cli/git_cmd.py` | 新建 | CLI 命令 `diff-stat` |
| `src/pydevman/__main__.py` | 修改 | 注册 `git_app` |
| `tests/git/test_diff.py` | 新建 | 核心逻辑单元测试 |

---

### Task 1：添加依赖 + 创建包骨架

**Files:**
- Modify: `pyproject.toml`
- Create: `src/pydevman/core/git/__init__.py`
- Create: `src/pydevman/core/git/diff.py`（骨架）
- Create: `tests/git/test_diff.py`（占位）

**Interfaces:**
- Produces: `pydevman.core.git` 包可被 import

- [ ] **Step 1：在 `pyproject.toml` 的 `dependencies` 中新增 gitpython**

找到以下位置（`pyproject.toml` 第 7-20 行），在列表末尾加一行：

```toml
dependencies = [
    "beautifulsoup4>=4.14.2",
    "inquirer>=3.4.0",
    "loguru>=0.7.3",
    "omegaconf>=2.3.0",
    "pydantic>=2.12.5",
    "pyperclip>=1.11.0",
    "requests>=2.32.5",
    "send2trash>=1.8.3",
    "sqlalchemy>=2.0.44",
    "tinydb>=4.8.2",
    "tomli>=2.3.0",
    "typer>=0.20.0",
    "gitpython>=3.1",
]
```

- [ ] **Step 2：安装依赖**

```bash
uv sync
```

预期：输出包含 `+ gitpython` 安装记录，无报错。

- [ ] **Step 3：创建空包文件**

```bash
mkdir -p src/pydevman/core/git
touch src/pydevman/core/git/__init__.py
```

- [ ] **Step 4：创建 `src/pydevman/core/git/diff.py` 骨架**

```python
"""core/git/diff.py — Git 分支差异分析"""
from __future__ import annotations

import re
import logging
from dataclasses import dataclass
from pathlib import Path

import git

log = logging.getLogger(__name__)
```

- [ ] **Step 5：创建 `tests/git/test_diff.py` 占位**

```bash
mkdir -p tests/git
touch tests/git/__init__.py
```

`tests/git/test_diff.py`：

```python
from pathlib import Path

# 以 pydevman 仓库自身作为测试 fixture
REPO_ROOT = Path(__file__).parent.parent.parent
```

- [ ] **Step 6：验证包可被 import**

```bash
uv run python -c "import pydevman.core.git; print('ok')"
```

预期输出：`ok`

- [ ] **Step 7：提交**

```bash
git add pyproject.toml uv.lock src/pydevman/core/git/ tests/git/
git commit -m "chore: add gitpython dep and core/git package scaffold"
```

---

### Task 2：DiffStat dataclass + resolve_base_branch

**Files:**
- Modify: `src/pydevman/core/git/diff.py`
- Modify: `tests/git/test_diff.py`

**Interfaces:**
- Consumes: Task 1 产出的 `diff.py` 骨架、`git.Repo`
- Produces:
  - `DiffStat(files_changed: int, added: int, deleted: int, base_branch: str, target_branch: str)` dataclass，含 `changed: int` 属性
  - `resolve_base_branch(repo: git.Repo) -> str`

- [ ] **Step 1：写失败测试**

在 `tests/git/test_diff.py` 追加：

```python
import git
from pydevman.core.git.diff import DiffStat, resolve_base_branch


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
```

- [ ] **Step 2：运行测试，确认失败**

```bash
uv run pytest tests/git/test_diff.py -v
```

预期：`ImportError: cannot import name 'DiffStat'`

- [ ] **Step 3：实现 DiffStat + resolve_base_branch**

在 `src/pydevman/core/git/diff.py` 骨架之后追加：

```python
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
```

- [ ] **Step 4：运行测试，确认通过**

```bash
uv run pytest tests/git/test_diff.py::test_diff_stat_dataclass tests/git/test_diff.py::test_resolve_base_branch_returns_main -v
```

预期：2 passed

- [ ] **Step 5：提交**

```bash
git add src/pydevman/core/git/diff.py tests/git/test_diff.py
git commit -m "feat: add DiffStat dataclass and resolve_base_branch"
```

---

### Task 3：diff_stat 函数

**Files:**
- Modify: `src/pydevman/core/git/diff.py`
- Modify: `tests/git/test_diff.py`

**Interfaces:**
- Consumes:
  - `DiffStat` (Task 2)
  - `resolve_base_branch(repo: git.Repo) -> str` (Task 2)
  - `_all_branch_names(repo: git.Repo) -> set[str]` (Task 2)
- Produces:
  - `diff_stat(project_dir: Path, target_branch: str, base_branch: str | None = None) -> DiffStat`

- [ ] **Step 1：写失败测试**

在 `tests/git/test_diff.py` 追加：

```python
from pydevman.core.git.diff import diff_stat


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
```

- [ ] **Step 2：运行测试，确认失败**

```bash
uv run pytest tests/git/test_diff.py -v -k "diff_stat"
```

预期：`ImportError: cannot import name 'diff_stat'`

- [ ] **Step 3：实现 `_parse_shortstat` + `diff_stat`**

在 `src/pydevman/core/git/diff.py` 末尾追加：

```python
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
```

- [ ] **Step 4：运行测试，确认通过**

```bash
uv run pytest tests/git/test_diff.py -v
```

预期：所有测试 passed

- [ ] **Step 5：提交**

```bash
git add src/pydevman/core/git/diff.py tests/git/test_diff.py
git commit -m "feat: implement diff_stat with shortstat parsing"
```

---

### Task 4：CLI git_cmd.py + 注册到 __main__.py

**Files:**
- Create: `src/pydevman/cli/git_cmd.py`
- Modify: `src/pydevman/__main__.py`

**Interfaces:**
- Consumes:
  - `diff_stat(project_dir: Path, target_branch: str, base_branch: str | None = None) -> DiffStat` (Task 3)
  - `api_build_table(title: str, header: list[str], rows: list) -> Table` from `pydevman.helper.table`
- Produces: `pydevman git diff-stat <project_dir> <target_branch> [--base <base_branch>]` CLI 命令

- [ ] **Step 1：创建 `src/pydevman/cli/git_cmd.py`**

```python
"""cli/git_cmd.py — Git 相关 CLI 命令"""

from pathlib import Path

import typer
from rich.console import Console
from typing_extensions import Annotated

from pydevman.core.git.diff import diff_stat
from pydevman.helper.table import api_build_table

console = Console()
app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

ARG_PROJECT_DIR = Annotated[Path, typer.Argument(help="Git 仓库根目录")]
ARG_TARGET_BRANCH = Annotated[str, typer.Argument(help="待分析分支")]
OPT_BASE_BRANCH = Annotated[
    str | None,
    typer.Option("--base", "-b", help="基准分支（默认自动检测 main/master）"),
]


@app.command("diff-stat", rich_help_panel="分析")
def cmd_diff_stat(
    project_dir: ARG_PROJECT_DIR,
    target_branch: ARG_TARGET_BRANCH,
    base_branch: OPT_BASE_BRANCH = None,
):
    """分析两个分支间的代码变更行数汇总"""
    console.rule("Git 分支差异分析")
    try:
        stat = diff_stat(project_dir.resolve(), target_branch, base_branch)
        rows = [
            ("变更文件数", str(stat.files_changed)),
            ("新增代码行数", str(stat.added)),
            ("删除代码行数", str(stat.deleted)),
            ("变更代码总行数", str(stat.changed)),
        ]
        title = f"{stat.base_branch}  →  {stat.target_branch}"
        table = api_build_table(title, ["指标", "数值"], rows)
        console.print(table)
    except Exception:
        console.print_exception()


if __name__ == "__main__":
    app()
```

- [ ] **Step 2：在 `__main__.py` 注册 git_app**

在 `src/pydevman/__main__.py` 中：

① 在 import 区末尾新增一行：
```python
from pydevman.cli.git_cmd import app as git_app
```

② 在 `main()` 函数中追加（紧跟 `file_app` 那行之后）：
```python
app.add_typer(git_app, name="git", help="git 工具")
```

修改后的 `main()` 完整内容：
```python
def main():
    app.add_typer(echo_app, name="echo", help="echo 工具")
    app.add_typer(json_app, name="json", help="json 工具")
    app.add_typer(file_app, name="file", help="file 工具")
    app.add_typer(git_app, name="git", help="git 工具")
    app()
```

- [ ] **Step 3：验证 CLI 帮助信息**

```bash
uv run pydevman git --help
```

预期输出含：
```
Commands:
  diff-stat  分析两个分支间的代码变更行数汇总
```

- [ ] **Step 4：端到端冒烟测试（对 pydevman 仓库自身运行）**

```bash
uv run pydevman git diff-stat . main --base main
```

预期：输出 rich 表格，所有数值为 0（同分支对比）：

```
             main  →  main
┌──────────────────┬──────┐
│ 指标              │ 数值  │
├──────────────────┼──────┤
│ 变更文件数        │ 0    │
│ 新增代码行数      │ 0    │
│ 删除代码行数      │ 0    │
│ 变更代码总行数    │ 0    │
└──────────────────┴──────┘
```

- [ ] **Step 5：运行全量测试，确认无回归**

```bash
uv run pytest -v
```

预期：所有测试 passed，无新增失败。

- [ ] **Step 6：提交**

```bash
git add src/pydevman/cli/git_cmd.py src/pydevman/__main__.py
git commit -m "feat: add git diff-stat CLI command"
```
