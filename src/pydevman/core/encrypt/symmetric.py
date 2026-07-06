"""
对称加密/解密模块
------------------
提供 AES 对称加密算法（CBC 和 GCM 模式）。
需要安装 cryptography 库：`pip install cryptography`

原理：
- AES-CBC：需要 IV（16字节），适合一般加密场景
- AES-GCM：认证加密（AEAD），自动检测数据是否被篡改，推荐使用
"""

import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# ============================================================================
# 内部常量与辅助函数
# ============================================================================

_AES_BLOCK_SIZE = 128  # AES 块大小（位）
_AES_BLOCK_BYTES = _AES_BLOCK_SIZE // 8  # 16 字节
_GCM_TAG_LENGTH = 16  # GCM 认证标签长度


def _pkcs7_pad(data: bytes, block_size: int = _AES_BLOCK_BYTES) -> bytes:
    """PKCS7 填充。"""
    padder = padding.PKCS7(block_size * 8).padder()
    return padder.update(data) + padder.finalize()


def _pkcs7_unpad(data: bytes, block_size: int = _AES_BLOCK_BYTES) -> bytes:
    """移除 PKCS7 填充。"""
    unpadder = padding.PKCS7(block_size * 8).unpadder()
    return unpadder.update(data) + unpadder.finalize()


# ============================================================================
# AES-CBC 模式
# ============================================================================


def aes_cbc_encrypt(plaintext: str | bytes, key: bytes, iv: bytes | None = None) -> tuple[bytes, bytes]:
    """使用 AES-CBC 模式加密数据。

    Args:
        plaintext: 明文字符串或字节
        key: 密钥，必须是 16/24/32 字节（对应 AES-128/192/256）
        iv: 初始化向量（16字节），不传则自动生成随机 IV

    Returns:
        (ciphertext, iv) 元组：密文字节 + 使用的 IV（解密时需提供）

    Raises:
        ValueError: 密钥长度不符合 AES 要求

    Examples:
        >>> key = os.urandom(32)  # AES-256
        >>> ciphertext, iv = aes_cbc_encrypt("hello world", key)
        >>> aes_cbc_decrypt(ciphertext, key, iv)
        'hello world'
    """
    if len(key) not in (16, 24, 32):
        raise ValueError(f"AES 密钥长度必须为 16/24/32 字节，当前为 {len(key)} 字节")

    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")

    if iv is None:
        iv = os.urandom(_AES_BLOCK_BYTES)

    plaintext = _pkcs7_pad(plaintext)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return ciphertext, iv


def aes_cbc_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> str:
    """使用 AES-CBC 模式解密数据。

    Args:
        ciphertext: 密文字节
        key: 密钥（需与加密时一致）
        iv: 加密时使用的 IV

    Returns:
        解密后的明文字符串

    Raises:
        ValueError: 密钥长度不符合 AES 要求
    """
    if len(key) not in (16, 24, 32):
        raise ValueError(f"AES 密钥长度必须为 16/24/32 字节，当前为 {len(key)} 字节")

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    plaintext = _pkcs7_unpad(plaintext)

    return plaintext.decode("utf-8")


# ============================================================================
# AES-GCM 模式（认证加密，推荐）
# ============================================================================


def aes_gcm_encrypt(
    plaintext: str | bytes,
    key: bytes,
    associated_data: bytes | None = None,
) -> tuple[bytes, bytes, bytes]:
    """使用 AES-GCM 模式加密数据（认证加密，推荐）。

    GCM 模式提供机密性和完整性保护，自动检测密文是否被篡改。

    Args:
        plaintext: 明文字符串或字节
        key: 密钥，必须是 16/24/32 字节（对应 AES-128/192/256）
        associated_data: 附加认证数据（AAD），不加密但参与完整性校验

    Returns:
        (nonce, ciphertext, tag) 元组——解密时三者都需要

    Raises:
        ValueError: 密钥长度不符合 AES 要求

    Examples:
        >>> key = os.urandom(32)
        >>> nonce, ct, tag = aes_gcm_encrypt("secret message", key)
        >>> aes_gcm_decrypt(nonce, ct, tag, key)
        'secret message'
    """
    if len(key) not in (16, 24, 32):
        raise ValueError(f"AES 密钥长度必须为 16/24/32 字节，当前为 {len(key)} 字节")

    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")

    nonce = os.urandom(12)  # GCM 推荐 12 字节 nonce

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    if associated_data:
        encryptor.authenticate_additional_data(associated_data)

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return nonce, ciphertext, encryptor.tag


def aes_gcm_decrypt(
    nonce: bytes,
    ciphertext: bytes,
    tag: bytes,
    key: bytes,
    associated_data: bytes | None = None,
) -> str:
    """使用 AES-GCM 模式解密数据。

    Args:
        nonce: 加密时使用的 nonce（12字节）
        ciphertext: 密文字节
        tag: 加密时生成的认证标签
        key: 密钥（需与加密时一致）
        associated_data: 附加认证数据（需与加密时一致，否则解密失败）

    Returns:
        解密后的明文字符串

    Raises:
        InvalidTag: 认证标签不匹配（密文被篡改或密钥错误）
        ValueError: 密钥长度不符合 AES 要求
    """
    if len(key) not in (16, 24, 32):
        raise ValueError(f"AES 密钥长度必须为 16/24/32 字节，当前为 {len(key)} 字节")

    cipher = Cipher(
        algorithms.AES(key),
        modes.GCM(nonce, tag),
        backend=default_backend(),
    )
    decryptor = cipher.decryptor()

    if associated_data:
        decryptor.authenticate_additional_data(associated_data)

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode("utf-8")
