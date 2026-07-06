"""JSON 模块 Web API — parse / dump"""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from pydevman.core.json.handler import (
    dump_json as _dump_json,
    filter_prefix as _filter_prefix,
    filter_suffix as _filter_suffix,
    parse_json as _parse_json,
    recursive_unescape as _recursive_unescape,
    strip_html_tags as _strip_html_tags,
)

router = APIRouter()


# ============================================================
# 请求 / 响应模型
# ============================================================

class ParseRequest(BaseModel):
    text: str = Field(..., description="待解析的 JSON 字符串")
    recursive: bool = Field(default=False, description="是否递归去转义")
    del_html_tag: bool = Field(default=False, description="是否去除 HTML 标签")
    prefix_filter: list[str] = Field(
        default_factory=list, description="需要过滤的字段前缀列表"
    )
    suffix_filter: list[str] = Field(
        default_factory=list, description="需要过滤的字段后缀列表"
    )
    inline: bool = Field(default=False, description="是否单行输出")


class ParseResponse(BaseModel):
    success: bool
    result: str | dict | list | None = None
    error: str | None = None


class DumpRequest(BaseModel):
    data: dict | list | str | int | float | bool | None = Field(
        ..., description="待序列化的 JSON 数据"
    )
    inline: bool = Field(default=False, description="是否单行输出")


class DumpResponse(BaseModel):
    success: bool
    result: str | None = None
    error: str | None = None


# ============================================================
# 路由
# ============================================================

@router.post("/parse", response_model=ParseResponse)
def parse_json(req: ParseRequest) -> ParseResponse:
    """解析 JSON 字符串，支持递归去转义、去标签、字段过滤"""
    try:
        data = _parse_json(req.text)
        if req.recursive:
            data = _recursive_unescape(data)
        if req.del_html_tag:
            data = _strip_html_tags(data)
        if req.prefix_filter:
            data = _filter_prefix(data, req.prefix_filter)
        if req.suffix_filter:
            data = _filter_suffix(data, req.suffix_filter)

        result = _dump_json(data, inline=req.inline)
        return ParseResponse(success=True, result=result)

    except Exception as e:
        return ParseResponse(success=False, error=str(e))


@router.post("/dump", response_model=DumpResponse)
def dump_json(req: DumpRequest) -> DumpResponse:
    """将 JSON 数据序列化为字符串"""
    try:
        result = _dump_json(req.data, inline=req.inline)
        return DumpResponse(success=True, result=result)
    except Exception as e:
        return DumpResponse(success=False, error=str(e))
