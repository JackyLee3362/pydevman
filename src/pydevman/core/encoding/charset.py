"""
字符编码检测与转换
------------------
提供字符集检测、编码转换、BOM 处理等函数。
"""

import codecs
import locale
from pathlib import Path


# ============================================================================
# 编码检测
# ============================================================================


def detect_bom(filepath: str | Path) -> str | None:
    """检测文件的 BOM（字节顺序标记）以判断文件编码。

    支持的 BOM：
        - UTF-8:    EF BB BF
        - UTF-16LE: FF FE
        - UTF-16BE: FE FF
        - UTF-32LE: FF FE 00 00
        - UTF-32BE: 00 00 FE FF

    Args:
        filepath: 文件路径

    Returns:
        编码名称，如 `utf-8-sig`、`utf-16`；未检测到时返回 None

    Examples:
        >>> detect_bom("utf8_with_bom.txt")
        'utf-8-sig'
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")

    with open(filepath, "rb") as f:
        head = f.read(4)

    if head[:3] == b"\xef\xbb\xbf":
        return "utf-8-sig"
    if head[:2] == b"\xff\xfe":
        if head[2:4] == b"\x00\x00":
            return "utf-32-le"
        return "utf-16-le"
    if head[:2] == b"\xfe\xff":
        return "utf-16-be"
    if head[:4] == b"\x00\x00\xfe\xff":
        return "utf-32-be"
    return None


def guess_file_encoding(filepath: str | Path, sample_size: int = 64 * 1024) -> str:
    """猜测文件的字符编码（启发式方法）。

    使用简单的启发式规则：
    1. 先检测 BOM
    2. 尝试 UTF-8 解码
    3. 检查是否为纯 ASCII
    4. 回退到系统默认编码

    注意：如需精确检测，推荐安装 `chardet` 库。

    Args:
        filepath: 文件路径
        sample_size: 采样读取的字节数

    Returns:
        猜测的编码名称

    Examples:
        >>> guess_file_encoding("unknown.txt")
        'gbk'
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")

    # 先检测 BOM
    bom_encoding = detect_bom(filepath)
    if bom_encoding:
        return bom_encoding

    # 读取样本
    with open(filepath, "rb") as f:
        raw = f.read(sample_size)

    # 尝试 UTF-8
    try:
        raw.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        pass

    # 检查纯 ASCII
    try:
        raw.decode("ascii")
        return "ascii"
    except UnicodeDecodeError:
        pass

    # 回退到系统默认编码
    return locale.getpreferredencoding()


# ============================================================================
# 编码转换
# ============================================================================


def convert_to_utf8(
    data: str | bytes,
    source_encoding: str | None = None,
) -> str:
    """将任意编码的文本转换为 UTF-8。

    Args:
        data: 字符串或字节
        source_encoding: 源编码，不传则自动检测

    Returns:
        UTF-8 编码的字符串

    Examples:
        >>> convert_to_utf8(b"\\xc4\\xe3\\xba\\xc3", source_encoding="gbk")
        '你好'
    """
    if isinstance(data, str):
        return data

    if source_encoding:
        return data.decode(source_encoding)

    # 自动尝试常见编码
    for enc in ("utf-8", "gbk", "gb2312", "gb18030", "latin-1"):
        try:
            return data.decode(enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
    # 最终回退
    return data.decode("utf-8", errors="replace")


def encode_to(
    text: str,
    target_encoding: str = "utf-8",
    errors: str = "strict",
) -> bytes:
    """将字符串编码为指定编码的字节。

    Args:
        text: 输入字符串
        target_encoding: 目标编码，默认 UTF-8
        errors: 错误处理策略（strict/ignore/replace/xmlcharrefreplace）

    Returns:
        编码后的字节

    Examples:
        >>> encode_to("你好", "gbk")
        b'\\xc4\\xe3\\xba\\xc3'
    """
    return text.encode(target_encoding, errors=errors)


def transcode(
    data: bytes,
    from_encoding: str,
    to_encoding: str,
) -> bytes:
    """将字节从一种编码转换为另一种编码。

    Args:
        data: 源编码的字节
        from_encoding: 源编码名称
        to_encoding: 目标编码名称

    Returns:
        目标编码的字节

    Examples:
        >>> transcode(b"\\xc4\\xe3\\xba\\xc3", "gbk", "utf-8")
        b'\\xe4\\xbd\\xa0\\xe5\\xa5\\xbd'
    """
    return data.decode(from_encoding).encode(to_encoding)


# ============================================================================
# Unicode 转义
# ============================================================================


def unicode_escape_encode(text: str) -> str:
    """将字符串中的非 ASCII 字符转为 Unicode 转义序列。

    Args:
        text: 输入字符串

    Returns:
        Unicode 转义后的字符串

    Examples:
        >>> unicode_escape_encode("你好abc")
        '\\\\u4f60\\\\u597dabc'
    """
    return text.encode("unicode_escape").decode("ascii")


def unicode_escape_decode(text: str) -> str:
    """将 Unicode 转义序列解码为原始字符串。

    Args:
        text: 含 Unicode 转义序列的字符串

    Returns:
        解码后的原始字符串

    Examples:
        >>> unicode_escape_decode("\\\\u4f60\\\\u597dabc")
        '你好abc'
    """
    return text.encode("ascii").decode("unicode_escape")


# ============================================================================
# 实用工具
# ============================================================================


def get_system_encoding() -> str:
    """获取当前系统的默认编码。

    Returns:
        系统默认编码名称

    Examples:
        >>> get_system_encoding()
        'gbk'  # 在中文 Windows 上
    """
    return locale.getpreferredencoding()


def is_valid_encoding(encoding_name: str) -> bool:
    """检查编码名称是否有效（Python 是否支持）。

    Args:
        encoding_name: 编码名称

    Returns:
        True 表示编码可用

    Examples:
        >>> is_valid_encoding("utf-8")
        True
        >>> is_valid_encoding("not-a-real-encoding")
        False
    """
    try:
        codecs.lookup(encoding_name)
        return True
    except LookupError:
        return False


def list_common_encodings() -> list[str]:
    """列出 Python 中常用的字符编码。

    Returns:
        常用编码名称列表
    """
    return [
        "utf-8",
        "utf-8-sig",
        "utf-16",
        "utf-16-le",
        "utf-16-be",
        "utf-32",
        "ascii",
        "latin-1",
        "iso-8859-1",
        "gbk",
        "gb2312",
        "gb18030",
        "big5",
        "shift_jis",
        "euc-jp",
        "euc-kr",
        "cp1252",
        "cp936",
        "cp950",
    ]
