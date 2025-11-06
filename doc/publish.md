---
type: basic-note
title: publish
author: JackyLee
create_time: 2025-11-06
update_time:
tags:
description:
---

## 发布流程

```sh
# 配置 pypi
cat ~/.pypirc
# 初始化环境
source ./venv/bin/activate
# 添加依赖
uv add [package]
# 添加开发依赖
uv add [package] --dev
# 编写代码
...
# 运行单测
...
# 构建
uv build
# 上传到本地
uv pip install dist/

# 上传到 pypi
twine upload dist/*
```

## **main**.py 函数

```sh
# 调用方法
# 设置环境变量
# windows
$env:PYTHONPATH="src"
# linux/macos
export PYTHONPATH=src
# .env
PYTHONPATH=src

# 然后
python -m src.pydevman --flag args...
```

## 类型问题

```py
# 3.9
def func(arg: Union[int, float]):

# 3.10
def func(arg: int | float):
```

## 参考资料
