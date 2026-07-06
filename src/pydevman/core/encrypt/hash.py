"""
哈希/摘要算法模块
--------------------
提供常用的哈希计算函数，包括 MD5、SHA 系列、BLAKE2、
文件哈希、HMAC 消息认证码等。
"""

import hashlib
import hmac
from pathlib import Path

# 文件分块读取大小
_CHUNK_SIZE = 64 * 1024  # 64KB


def md5(text: str | bytes) -> str:
    """计算字符串/字节的 MD5 哈希值。

    Args:
        text: 输入字符串或字节

    Returns:
        MD5 哈希值的十六进制字符串（32位）

    Examples:
        >>> md5("hello")
        '5d41402abc4b2a76b9719d911017c592'
    """
    if isinstance(text, str):
        text = text.encode("utf-8")
    return hashlib.md5(text).hexdigest()


def sha1(text: str | bytes) -> str:
    """计算字符串/字节的 SHA1 哈希值。

    Args:
        text: 输入字符串或字节

    Returns:
        SHA1 哈希值的十六进制字符串（40位）

    Examples:
        >>> sha1("hello")
        'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d'
    """
    if isinstance(text, str):
        text = text.encode("utf-8")
    return hashlib.sha1(text).hexdigest()


def sha256(text: str | bytes) -> str:
    """计算字符串/字节的 SHA256 哈希值。

    Args:
        text: 输入字符串或字节

    Returns:
        SHA256 哈希值的十六进制字符串（64位）

    Examples:
        >>> sha256("hello")
        '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    """
    if isinstance(text, str):
        text = text.encode("utf-8")
    return hashlib.sha256(text).hexdigest()


def sha512(text: str | bytes) -> str:
    """计算字符串/字节的 SHA512 哈希值。

    Args:
        text: 输入字符串或字节

    Returns:
        SHA512 哈希值的十六进制字符串（128位）
    """
    if isinstance(text, str):
        text = text.encode("utf-8")
    return hashlib.sha512(text).hexdigest()


def blake2b(text: str | bytes, digest_size: int = 64) -> str:
    """计算字符串/字节的 BLAKE2b 哈希值（比 SHA3 更快）。

    Args:
        text: 输入字符串或字节
        digest_size: 摘要长度（1~64 字节），默认 64

    Returns:
        BLAKE2b 哈希值的十六进制字符串
    """
    if isinstance(text, str):
        text = text.encode("utf-8")
    return hashlib.blake2b(text, digest_size=digest_size).hexdigest()


def file_md5(filepath: str | Path) -> str:
    """计算文件的 MD5 哈希值（分块读取，适用于大文件）。

    Args:
        filepath: 文件路径

    Returns:
        文件的 MD5 哈希值（32位十六进制字符串）

    Raises:
        FileNotFoundError: 文件不存在时抛出
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")

    md5_hash = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(_CHUNK_SIZE):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def file_sha256(filepath: str | Path) -> str:
    """计算文件的 SHA256 哈希值（分块读取，适用于大文件）。

    Args:
        filepath: 文件路径

    Returns:
        文件的 SHA256 哈希值（64位十六进制字符串）

    Raises:
        FileNotFoundError: 文件不存在时抛出
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")

    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(_CHUNK_SIZE):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def hmac_sha256(key: str | bytes, message: str | bytes) -> str:
    """计算 HMAC-SHA256 消息认证码。

    用于验证消息的完整性和真实性。

    Args:
        key: 密钥（双方共享的密钥）
        message: 消息内容

    Returns:
        HMAC-SHA256 值的十六进制字符串（64位）

    Examples:
        >>> hmac_sha256("secret-key", "hello world")
        '4e5130e6f5e3c1c0b5a0d9e4f...'
    """
    if isinstance(key, str):
        key = key.encode("utf-8")
    if isinstance(message, str):
        message = message.encode("utf-8")
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def hmac_sha512(key: str | bytes, message: str | bytes) -> str:
    """计算 HMAC-SHA512 消息认证码。

    Args:
        key: 密钥（双方共享的密钥）
        message: 消息内容

    Returns:
        HMAC-SHA512 值的十六进制字符串（128位）
    """
    if isinstance(key, str):
        key = key.encode("utf-8")
    if isinstance(message, str):
        message = message.encode("utf-8")
    return hmac.new(key, message, hashlib.sha512).hexdigest()


def sha256_digest(text: str | bytes) -> bytes:
    """计算 SHA256 并返回原始字节（非十六进制字符串）。

    Args:
        text: 输入

    Returns:
        SHA256 的原始字节摘要
    """
    if isinstance(text, str):
        text = text.encode("utf-8")
    return hashlib.sha256(text).digest()
