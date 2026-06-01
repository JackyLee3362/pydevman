from typing import Iterable

from pydantic import BaseModel


class JsonConfig(BaseModel):
    recursive: bool = False

    del_tag: bool = False

    prefix: Iterable[str] = None

    suffix: Iterable[str] = None
