"""
加密工具函数模块
----------------
提供密钥生成、安全随机数、常量时间比较等实用工具。
"""

import hashlib
import os
import secrets
import string


def generate_random_bytes(length: int = 32) -> bytes:
    """生成加密安全的随机字节。

    Args:
        length: 字节长度，默认 32

    Returns:
        随机字节串
    """
    return os.urandom(length)


def generate_random_key(length: int = 32) -> str:
    """生成随机密钥（十六进制字符串）。

    Args:
        length: 密钥字节长度，默认 32（输出 64 位十六进制字符串）

    Returns:
        十六进制格式的随机密钥字符串

    Examples:
        >>> key = generate_random_key()
        >>> len(key)
        64
    """
    return secrets.token_hex(length)


def generate_token(length: int = 32) -> str:
    """生成 URL 安全的随机令牌。

    适用于生成 API Key、Session Token、CSRF Token 等。

    Args:
        length: 令牌字节长度，默认 32

    Returns:
        URL 安全的随机令牌字符串
    """
    return secrets.token_urlsafe(length)


def generate_password(length: int = 16, *, digits: bool = True, punctuation: bool = True) -> str:
    """生成随机密码。

    Args:
        length: 密码长度
        digits: 是否包含数字，默认 True
        punctuation: 是否包含特殊字符，默认 True

    Returns:
        随机密码字符串
    """
    alphabet = string.ascii_letters
    if digits:
        alphabet += string.digits
    if punctuation:
        alphabet += string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(length))


def derive_key(
    password: str,
    salt: bytes | None = None,
    iterations: int = 600_000,
    key_length: int = 32,
) -> tuple[bytes, bytes]:
    """使用 PBKDF2（基于 SHA256）从密码派生密钥。

    Args:
        password: 密码
        salt: 盐值（字节），不传则自动生成 16 字节随机盐
        iterations: PBKDF2 迭代次数，默认 600,000
        key_length: 派生密钥长度（字节），默认 32

    Returns:
        (derived_key, salt) 元组——派生密钥和使用的盐值

    Examples:
        >>> key, salt = derive_key("my-password")
        >>> len(key), len(salt)
        (32, 16)
    """
    if salt is None:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
        dklen=key_length,
    )
    return key, salt


def verify_derived_key(
    password: str,
    salt: bytes,
    target_key: bytes,
    iterations: int = 600_000,
    key_length: int = 32,
) -> bool:
    """验证给定密码是否匹配派生密钥（常数时间比较）。

    用于密码存储的校验场景——数据库中存储 salt + derived_key，
    用户登录时用输入的密码重新计算并与存储值比对。

    Args:
        password: 待验证的密码
        salt: 原始盐值
        target_key: 存储的派生密钥
        iterations: PBKDF2 迭代次数（需与 derive_key 时一致）
        key_length: 密钥长度（需与 derive_key 时一致）

    Returns:
        密码是否匹配
    """
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
        dklen=key_length,
    )
    return constant_time_compare(derived, target_key)


def constant_time_compare(a: bytes | str, b: bytes | str) -> bool:
    """常数时间比较两个值（防止时序攻击）。

    对于字符串输入，先编码为 UTF-8 再比较。

    Args:
        a: 第一个值
        b: 第二个值

    Returns:
        两个值是否相等
    """
    if isinstance(a, str):
        a = a.encode("utf-8")
    if isinstance(b, str):
        b = b.encode("utf-8")
    return secrets.compare_digest(a, b)
