"""
二进制/文本编解码
------------------
提供 Base64、Base32、Base16（Hex）等常用二进制编解码函数。
"""

import base64
import binascii


# ============================================================================
# Base64 编解码
# ============================================================================


def base64_encode(data: str | bytes) -> str:
    """将字符串/字节编码为 Base64 字符串。

    Args:
        data: 待编码的字符串或字节

    Returns:
        Base64 编码后的字符串

    Examples:
        >>> base64_encode("hello")
        'aGVsbG8='
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return base64.b64encode(data).decode("utf-8")


def base64_decode(data: str | bytes) -> str:
    """将 Base64 字符串解码为原始字符串。

    Args:
        data: Base64 编码的字符串或字节

    Returns:
        解码后的原始字符串

    Raises:
        binascii.Error: 解码失败（非法 Base64 输入）

    Examples:
        >>> base64_decode("aGVsbG8=")
        'hello'
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return base64.b64decode(data).decode("utf-8")


def base64_decode_bytes(data: str | bytes) -> bytes:
    """将 Base64 字符串解码为原始字节。

    Args:
        data: Base64 编码的字符串或字节

    Returns:
        解码后的原始字节
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return base64.b64decode(data)


# ============================================================================
# URL 安全的 Base64 编解码
# ============================================================================


def urlsafe_base64_encode(data: str | bytes) -> str:
    """将字符串/字节编码为 URL 安全的 Base64（无 `+`、`/` 和 `=` 填充）。

    适用于在 URL 路径、文件名或 JWT 中传输数据。

    Args:
        data: 待编码的字符串或字节

    Returns:
        URL 安全的 Base64 字符串

    Examples:
        >>> urlsafe_base64_encode("hello")
        'aGVsbG8'
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def urlsafe_base64_decode(data: str | bytes) -> str:
    """将 URL 安全的 Base64 字符串解码为原始字符串。

    自动补全缺失的 `=` 填充符。

    Args:
        data: URL 安全的 Base64 字符串

    Returns:
        解码后的原始字符串
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    # 自动补充 = 填充
    missing_padding = len(data) % 4
    if missing_padding:
        data += b"=" * (4 - missing_padding)
    return base64.urlsafe_b64decode(data).decode("utf-8")


# ============================================================================
# Base32 编解码
# ============================================================================


def base32_encode(data: str | bytes) -> str:
    """将字符串/字节编码为 Base32 字符串。

    Args:
        data: 待编码的字符串或字节

    Returns:
        Base32 编码后的字符串
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return base64.b32encode(data).decode("utf-8")


def base32_decode(data: str | bytes) -> str:
    """将 Base32 字符串解码为原始字符串。

    Args:
        data: Base32 编码的字符串或字节

    Returns:
        解码后的原始字符串
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    # 自动补充 = 填充
    missing_padding = len(data) % 8
    if missing_padding:
        data += b"=" * (8 - missing_padding)
    return base64.b32decode(data).decode("utf-8")


# ============================================================================
# Base16 / Hex（十六进制）编解码
# ============================================================================


def hex_encode(data: str | bytes) -> str:
    """将字符串/字节编码为十六进制字符串。

    Args:
        data: 待编码的字符串或字节

    Returns:
        十六进制字符串（小写）

    Examples:
        >>> hex_encode("hello")
        '68656c6c6f'
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return data.hex()


def hex_decode(hex_str: str) -> bytes:
    """将十六进制字符串解码为原始字节。

    Args:
        hex_str: 十六进制字符串（大小写均可，可含空格）

    Returns:
        解码后的原始字节

    Raises:
        binascii.Error: 解码失败（非法十六进制输入）
    """
    hex_str = hex_str.strip().replace(" ", "")
    return binascii.unhexlify(hex_str)


def hex_decode_str(hex_str: str) -> str:
    """将十六进制字符串解码为 UTF-8 字符串。

    Args:
        hex_str: 十六进制字符串

    Returns:
        解码后的 UTF-8 字符串
    """
    return hex_decode(hex_str).decode("utf-8")


# ============================================================================
# Base85 / ASCII85 编解码
# ============================================================================


def base85_encode(data: str | bytes) -> str:
    """将字符串/字节编码为 Base85（ASCII85）字符串。

    比 Base64 更紧凑，适合在 ASCII 环境中传输二进制数据。

    Args:
        data: 待编码的字符串或字节

    Returns:
        Base85 编码后的字符串

    Examples:
        >>> base85_encode("hello")
        'BOu!rD]j7BEbo7'
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return base64.a85encode(data).decode("utf-8")


def base85_decode(data: str | bytes) -> str:
    """将 Base85 字符串解码为原始字符串。

    Args:
        data: Base85 编码的字符串或字节

    Returns:
        解码后的原始字符串
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return base64.a85decode(data).decode("utf-8")
