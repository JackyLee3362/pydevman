"""
编码格式枚举
------------
定义所有支持的编解码格式，及其对应的编码/解码函数映射，供 CLI 及其他模块统一引用。
"""

from enum import StrEnum


class EncodingFormat(StrEnum):
    """支持的编解码格式。

    每个枚举值对应一种编码/解码算法，可直接作为 ``--format`` 参数值使用。
    """

    BASE64 = "base64"
    """Base64 编解码"""

    URLSAFE_BASE64 = "urlsafe_base64"
    """URL 安全的 Base64（无 ``+``、``/``、``=``）"""

    BASE32 = "base32"
    """Base32 编解码"""

    BASE85 = "base85"
    """Base85 / ASCII85 编解码"""

    HEX = "hex"
    """十六进制（Hex）编解码"""

    URL = "url"
    """URL 百分号编码（空格 → ``%20``）"""

    URL_PLUS = "url_plus"
    """form-urlencoded 编码（空格 → ``+``）"""

    UNICODE_ESCAPE = "unicode_escape"
    """Unicode 转义序列（``\\uXXXX``）"""

    @property
    def encode_func(self) -> str:
        """返回该格式对应的编码函数名（位于 ``pydevman.core.encoding`` 模块中）。"""
        return ENCODE_MAP[self]

    @property
    def decode_func(self) -> str:
        """返回该格式对应的解码函数名（位于 ``pydevman.core.encoding`` 模块中）。"""
        return DECODE_MAP[self]

    @property
    def description(self) -> str:
        """返回该格式的简要描述。"""
        return _DESCRIPTIONS.get(self, "")


# ---- 编码/解码函数名映射 ----

ENCODE_MAP: dict[EncodingFormat, str] = {
    EncodingFormat.BASE64: "base64_encode",
    EncodingFormat.URLSAFE_BASE64: "urlsafe_base64_encode",
    EncodingFormat.BASE32: "base32_encode",
    EncodingFormat.BASE85: "base85_encode",
    EncodingFormat.HEX: "hex_encode",
    EncodingFormat.URL: "url_encode",
    EncodingFormat.URL_PLUS: "url_encode_plus",
    EncodingFormat.UNICODE_ESCAPE: "unicode_escape_encode",
}

DECODE_MAP: dict[EncodingFormat, str] = {
    EncodingFormat.BASE64: "base64_decode",
    EncodingFormat.URLSAFE_BASE64: "urlsafe_base64_decode",
    EncodingFormat.BASE32: "base32_decode",
    EncodingFormat.BASE85: "base85_decode",
    EncodingFormat.HEX: "hex_decode_str",
    EncodingFormat.URL: "url_decode",
    EncodingFormat.URL_PLUS: "url_decode_plus",
    EncodingFormat.UNICODE_ESCAPE: "unicode_escape_decode",
}

_DESCRIPTIONS: dict[EncodingFormat, str] = {
    EncodingFormat.BASE64: "Base64 编解码",
    EncodingFormat.URLSAFE_BASE64: "URL 安全 Base64",
    EncodingFormat.BASE32: "Base32 编解码",
    EncodingFormat.BASE85: "Base85/ASCII85 编解码",
    EncodingFormat.HEX: "十六进制编解码",
    EncodingFormat.URL: "URL 百分号编码 (%20)",
    EncodingFormat.URL_PLUS: "form-urlencoded (+)",
    EncodingFormat.UNICODE_ESCAPE: "Unicode 转义 (\\uXXXX)",
}
