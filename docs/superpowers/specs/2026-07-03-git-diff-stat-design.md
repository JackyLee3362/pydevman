# Design: core/git diff-stat 模块

**日期：** 2026-07-03  
**状态：** 已确认

---

## 背景

pydevman 需要新增一个 `core/git` 模块，用于分析两个 Git 分支之间的代码变更情况，输出汇总报告（新增行数、删除行数、变更文件数），同时提供配套 CLI 命令。

---

## 需求

| 输入 | 说明 |
|---|---|
| `project_dir: Path` | Git 仓库根目录 |
| `target_branch: str` | 待分析分支 |
| `base_branch: str \| None` | 基准分支；`None` 时自动检测，优先 `main`，其次 `master` |

| 输出字段 | 类型 | 说明 |
|---|---|---|
| `files_changed` | `int` | 变更文件数 |
| `added` | `int` | 新增代码行数 |
| `deleted` | `int` | 删除代码行数 |
| `changed` | `int` | `added + deleted`（属性，自动计算） |
| `base_branch` | `str` | 实际使用的基准分支 |
| `target_branch` | `str` | 待分析分支 |

---

## 文件结构

```
src/pydevman/
├── core/
│   └── git/
│       ├── __init__.py      # 空文件
│       └── diff.py          # 核心逻辑
└── cli/
    └── git_cmd.py           # CLI 命令
```

`pyproject.toml` 新增依赖：`gitpython>=3.1`

---

## 核心逻辑（`core/git/diff.py`）

### 数据模型

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
```

### `resolve_base_branch(repo: git.Repo) -> str`

1. 获取所有本地分支名和远端分支名（去掉 `origin/` 前缀）
2. 依次检测 `main`、`master` 是否存在
3. 找到则返回分支名；均不存在则 `raise ValueError("无法自动检测基准分支，请手动指定 --base")`

### `diff_stat(project_dir: Path, target_branch: str, base_branch: str | None = None) -> DiffStat`

1. `repo = git.Repo(project_dir)` — 非 Git 仓库抛 `git.InvalidGitRepositoryError`
2. `base_branch` 为 `None` 时调用 `resolve_base_branch(repo)`
3. 校验 `target_branch` 在本地或远端分支中存在，否则 `raise ValueError(f"分支不存在: {target_branch}")`
4. 调用 `repo.git.diff('--shortstat', base_branch, target_branch)` 获取输出文本
5. 正则解析：`r'(\d+) files? changed(?:, (\d+) insertions?)?(?:, (\d+) deletions?)?'`
6. 返回 `DiffStat`

**`--shortstat` 输出示例：**
```
 3 files changed, 42 insertions(+), 7 deletions(-)
```

> 注意：若两个分支完全相同，`--shortstat` 输出为空字符串，此时返回全零的 `DiffStat`。

---

## CLI（`cli/git_cmd.py`）

```
pydevman git diff-stat <project_dir> <target_branch> [--base <base_branch>]
```

输出风格与 `file_cmd.py` 一致，使用 `rich` 表格：

```
┌──────────────────┬──────┐
│ 指标              │ 数值  │
├──────────────────┼──────┤
│ 变更文件数        │ 3    │
│ 新增代码行数      │ 42   │
│ 删除代码行数      │ 7    │
│ 变更代码总行数    │ 49   │
└──────────────────┴──────┘
```

`--base` 为可选参数，不传时自动检测 `main` / `master`。

---

## 错误处理

| 错误情况 | 处理方式 |
|---|---|
| `project_dir` 不是 Git 仓库 | `git.InvalidGitRepositoryError` 向上抛出，CLI 层 `console.print_exception()` 捕获 |
| `target_branch` 不存在 | `raise ValueError(f"分支不存在: {target_branch}")` |
| 无法自动检测基准分支 | `raise ValueError("无法自动检测基准分支，请手动指定 --base")` |
| 两分支完全相同 | 正常返回，所有字段为 0 |

---

## 依赖变更

`pyproject.toml` `[project.dependencies]` 新增：

```toml
"gitpython>=3.1",
```

---

## 不在范围内

- 按文件细分报告（当前仅汇总）
- 远端分支 fetch（仅使用本地已有的分支信息）
- 二进制文件行数统计
