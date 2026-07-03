"""core/git/diff.py — Git 分支差异分析"""
from __future__ import annotations

import re
import logging
from dataclasses import dataclass
from pathlib import Path

import git

log = logging.getLogger(__name__)
