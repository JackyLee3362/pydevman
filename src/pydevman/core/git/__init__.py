"""core/git package"""
# Import gitpython explicitly to avoid shadowing by local tests.git package
from git import Repo

__all__ = ["Repo"]
