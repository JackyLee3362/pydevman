"""
编解码模块
==========
提供常用的编解码函数，按功能分为以下子模块：

- binary.py   二进制编解码（Base64、Base32、Base85、Hex）
- url.py      URL 编解码（百分号编码、Query String 解析）
- charset.py  字符编码检测与转换（BOM 检测、编码转换、Unicode 转义）
- enum.py     编解码格式枚举（供 CLI 等模块统一引用）
"""

# ---- 枚举 ----
from pydevman.core.encoding.enum import EncodingFormat

# ---- 二进制编解码 ----
from pydevman.core.encoding.binary import (
    base32_decode,
    base32_encode,
    base64_decode,
    base64_decode_bytes,
    base64_encode,
    base85_decode,
    base85_encode,
    hex_decode,
    hex_decode_str,
    hex_encode,
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)

# ---- URL 编解码 ----
from pydevman.core.encoding.url import (
    build_query_string,
    parse_query_string,
    url_decode,
    url_decode_plus,
    url_encode,
    url_encode_plus,
    url_parse,
    url_unparse,
)

# ---- 字符编码 ----
from pydevman.core.encoding.charset import (
    convert_to_utf8,
    detect_bom,
    encode_to,
    get_system_encoding,
    guess_file_encoding,
    is_valid_encoding,
    list_common_encodings,
    transcode,
    unicode_escape_decode,
    unicode_escape_encode,
)

__all__ = [
    # 枚举
    "EncodingFormat",
    # 二进制编解码
    "base64_encode",
    "base64_decode",
    "base64_decode_bytes",
    "urlsafe_base64_encode",
    "urlsafe_base64_decode",
    "base32_encode",
    "base32_decode",
    "base85_encode",
    "base85_decode",
    "hex_encode",
    "hex_decode",
    "hex_decode_str",
    # URL 编解码
    "url_encode",
    "url_decode",
    "url_encode_plus",
    "url_decode_plus",
    "parse_query_string",
    "build_query_string",
    "url_parse",
    "url_unparse",
    # 字符编码
    "detect_bom",
    "guess_file_encoding",
    "convert_to_utf8",
    "encode_to",
    "transcode",
    "unicode_escape_encode",
    "unicode_escape_decode",
    "get_system_encoding",
    "is_valid_encoding",
    "list_common_encodings",
]
