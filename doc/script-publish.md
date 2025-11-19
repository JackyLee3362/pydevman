---
type: basic-note
title: script-publish
author: JackyLee
create_time: 2025-11-18
update_time:
tags:
description:
---

## 发布可执行程序

```toml
[project.scripts]
dev = "pydevman.__main__:main"
```

在本地测试

```sh
uv pip install --editable .
# 然后
.venv/bin/dev

# 一条命令
uv build; uv pip install --editable .
```

## 参考资料
