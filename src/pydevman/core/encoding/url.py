"""
URL 编解码
----------
提供 URL 百分号编码（percent-encoding）与解码，
以及 Query String 的解析与构建。
"""

import urllib.parse


# ============================================================================
# URL 编码（Percent-Encoding）
# ============================================================================


def url_encode(text: str, safe: str = "") -> str:
    """对字符串进行 URL 百分号编码。

    将特殊字符转换为 `%XX` 格式（如空格 → `%20`）。

    Args:
        text: 待编码的字符串
        safe: 不编码的安全字符（除默认的字母、数字、`_.-` 之外）

    Returns:
        URL 编码后的字符串

    Examples:
        >>> url_encode("hello world")
        'hello%20world'
        >>> url_encode("你好")
        '%E4%BD%A0%E5%A5%BD'
        >>> url_encode("a/b/c", safe="/")
        'a/b/c'
    """
    return urllib.parse.quote(text, safe=safe)


def url_decode(text: str) -> str:
    """对 URL 百分号编码字符串进行解码。

    Args:
        text: URL 编码的字符串

    Returns:
        解码后的原始字符串

    Examples:
        >>> url_decode("hello%20world")
        'hello world'
        >>> url_decode("%E4%BD%A0%E5%A5%BD")
        '你好'
    """
    return urllib.parse.unquote(text)


# ============================================================================
# URL 路径编码（更激进，编码 `/`）
# ============================================================================


def url_encode_plus(text: str) -> str:
    """类似 `application/x-www-form-urlencoded` 的编码方式。

    空格编码为 `+` 而非 `%20`。

    Args:
        text: 待编码的字符串

    Returns:
        编码后的字符串

    Examples:
        >>> url_encode_plus("hello world")
        'hello+world'
    """
    return urllib.parse.quote_plus(text)


def url_decode_plus(text: str) -> str:
    """解码 `application/x-www-form-urlencoded` 格式的字符串。

    `+` 解码为空格。

    Args:
        text: 编码的字符串

    Returns:
        解码后的字符串

    Examples:
        >>> url_decode_plus("hello+world")
        'hello world'
    """
    return urllib.parse.unquote_plus(text)


# ============================================================================
# Query String 解析与构建
# ============================================================================


def parse_query_string(query: str) -> dict[str, list[str]]:
    """解析 URL 查询字符串为字典。

    Args:
        query: URL 查询字符串（不含开头的 `?`）

    Returns:
        参数名到值列表的映射字典

    Examples:
        >>> parse_query_string("name=Alice&age=20&tag=py&tag=web")
        {'name': ['Alice'], 'age': ['20'], 'tag': ['py', 'web']}
    """
    return urllib.parse.parse_qs(query)


def build_query_string(params: dict[str, str | list[str]], doseq: bool = False) -> str:
    """将字典构建为 URL 查询字符串。

    Args:
        params: 参数字典
        doseq: 是否将列表值展开为多个同名参数

    Returns:
        URL 查询字符串（不含开头的 `?`）

    Examples:
        >>> build_query_string({"name": "Alice", "age": "20"})
        'name=Alice&age=20'
        >>> build_query_string({"tag": ["py", "web"]}, doseq=True)
        'tag=py&tag=web'
    """
    return urllib.parse.urlencode(params, doseq=doseq)


def url_parse(url: str) -> urllib.parse.ParseResult:
    """解析 URL 为各组成部分（scheme, netloc, path, params, query, fragment）。

    Args:
        url: 完整的 URL 字符串

    Returns:
        ParseResult 命名元组

    Examples:
        >>> r = url_parse("https://example.com/path?q=1#frag")
        >>> r.scheme
        'https'
        >>> r.netloc
        'example.com'
        >>> r.path
        '/path'
        >>> r.query
        'q=1'
    """
    return urllib.parse.urlparse(url)


def url_unparse(parsed: urllib.parse.ParseResult) -> str:
    """将 ParseResult 重新组合为 URL 字符串。

    Args:
        parsed: url_parse 的返回结果

    Returns:
        完整的 URL 字符串
    """
    return urllib.parse.urlunparse(parsed)
