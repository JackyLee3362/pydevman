---
type: basic-note
title: pypi
author: JackyLee
create_time: 2025-11-07
update_time:
tags:
description:
---

## PyPI 支持上传 SNAPSHOT 吗？

PyPI 不允许重复上传同一版本号，不支持 snapshot (快照)版本

PyPI 上发布 snapshot 的主流做法是通过版本号标识快照，添加如 dev, alpha, beta, rc 等后缀，如：

- 1.2.3.dev20240101
- 2.0.0a1
- 0.9.0b2

这种命名不会影响上传，但这只是“预发布版”或“开发版”，不是真正的可变“快照版”。

推荐在快照版本里添加日期时间或构建号保证唯一性，如：0.3.1.dev202406251100。

若想持续发布临时快照，可以自动递增版本或打包时间戳，每次为不同版本号。例如使用 setuptools_scm 自动生成 dev 版号。

## 如何发布私有或者测试 PyPI

- 测试 PyPI: :可上传任意测试版或快照，不影响正式 PyPI 项目。
- 私有 PyPI:使用 devpi 或 pypiserver 自建私服，可以无限制发布/覆盖同一包版本快照，适合内部集成和交付。

```sh
# 测试 PyPI 网址: https://test.pypi.org/
twine upload --repository testpypi dist/*

# 安装时需要指定源
pip install --index-url https://test.pypi.org/simple/ your-package-name
```

## 参考资料
