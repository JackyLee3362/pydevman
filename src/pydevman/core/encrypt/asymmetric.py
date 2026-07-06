"""
非对称加密/解密与签名模块
--------------------------
提供 RSA 密钥生成、加解密、签名与验签功能。
需要安装 cryptography 库：`pip install cryptography`

原理：
- 公钥加密，私钥解密——用于数据传输
- 私钥签名，公钥验签——用于身份验证与数据完整性
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.padding import (
    MGF1,
    OAEP,
    PSS,
    PKCS1v15,
)


# ============================================================================
# RSA 密钥生成与序列化
# ============================================================================


def generate_rsa_key_pair(key_size: int = 2048) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """生成 RSA 密钥对。

    Args:
        key_size: 密钥长度（位），推荐 2048 或 4096

    Returns:
        (private_key, public_key) 元组

    Examples:
        >>> priv, pub = generate_rsa_key_pair(2048)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    public_key = private_key.public_key()
    return private_key, public_key


def private_key_to_pem(private_key: rsa.RSAPrivateKey, password: bytes | None = None) -> bytes:
    """将 RSA 私钥序列化为 PEM 格式字节。

    Args:
        private_key: RSA 私钥对象
        password: 用于加密私钥的密码，不传则不加密

    Returns:
        PEM 格式的私钥字节
    """
    encryption = (
        serialization.BestAvailableEncryption(password)
        if password
        else serialization.NoEncryption()
    )
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption,
    )


def public_key_to_pem(public_key: rsa.RSAPublicKey) -> bytes:
    """将 RSA 公钥序列化为 PEM 格式字节。

    Args:
        public_key: RSA 公钥对象

    Returns:
        PEM 格式的公钥字节
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def load_private_key_from_pem(pem_data: bytes, password: bytes | None = None) -> rsa.RSAPrivateKey:
    """从 PEM 字节加载 RSA 私钥。

    Args:
        pem_data: PEM 格式的私钥字节
        password: 私钥密码（如生成时设置了密码则需提供）

    Returns:
        RSA 私钥对象
    """
    return serialization.load_pem_private_key(
        pem_data,
        password=password,
        backend=default_backend(),
    )


def load_public_key_from_pem(pem_data: bytes) -> rsa.RSAPublicKey:
    """从 PEM 字节加载 RSA 公钥。

    Args:
        pem_data: PEM 格式的公钥字节

    Returns:
        RSA 公钥对象
    """
    return serialization.load_pem_public_key(
        pem_data,
        backend=default_backend(),
    )


# ============================================================================
# RSA 加密/解密（OAEP 填充，推荐）
# ============================================================================


def rsa_encrypt(plaintext: str | bytes, public_key: rsa.RSAPublicKey) -> bytes:
    """使用 RSA 公钥加密数据（OAEP 填充，推荐）。

    注意：RSA 单次加密数据长度有限（密钥位数/8 - 2*hash_size - 2 字节）。
    例如 2048 位密钥约 190 字节。大数据请使用混合加密：用 AES 加密数据，用 RSA 加密 AES 密钥。

    Args:
        plaintext: 明文（字符串或字节）
        public_key: RSA 公钥

    Returns:
        密文字节

    Examples:
        >>> priv, pub = generate_rsa_key_pair()
        >>> ct = rsa_encrypt("hello", pub)
        >>> rsa_decrypt(ct, priv)
        'hello'
    """
    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")

    ciphertext = public_key.encrypt(
        plaintext,
        OAEP(
            mgf=MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext


def rsa_decrypt(ciphertext: bytes, private_key: rsa.RSAPrivateKey) -> str:
    """使用 RSA 私钥解密数据。

    Args:
        ciphertext: 密文字节
        private_key: RSA 私钥

    Returns:
        解密后的明文字符串
    """
    plaintext = private_key.decrypt(
        ciphertext,
        OAEP(
            mgf=MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return plaintext.decode("utf-8")


# ============================================================================
# RSA 签名/验签
# ============================================================================


def rsa_sign(
    message: str | bytes,
    private_key: rsa.RSAPrivateKey,
    algorithm: hashes.HashAlgorithm | None = None,
) -> bytes:
    """使用 RSA 私钥对消息进行数字签名（PSS 填充）。

    Args:
        message: 待签名的消息
        private_key: RSA 私钥
        algorithm: 哈希算法，默认 SHA256

    Returns:
        签名字节

    Examples:
        >>> priv, pub = generate_rsa_key_pair()
        >>> sig = rsa_sign("hello", priv)
        >>> rsa_verify("hello", sig, pub)
        True
    """
    if isinstance(message, str):
        message = message.encode("utf-8")
    if algorithm is None:
        algorithm = hashes.SHA256()

    signature = private_key.sign(
        message,
        PSS(
            mgf=MGF1(algorithm),
            salt_length=PSS.MAX_LENGTH,
        ),
        algorithm,
    )
    return signature


def rsa_verify(
    message: str | bytes,
    signature: bytes,
    public_key: rsa.RSAPublicKey,
    algorithm: hashes.HashAlgorithm | None = None,
) -> bool:
    """使用 RSA 公钥验证数字签名。

    Args:
        message: 原始消息
        signature: 签名字节
        public_key: RSA 公钥
        algorithm: 哈希算法，需与签名时一致（默认 SHA256）

    Returns:
        签名是否有效

    Examples:
        >>> priv, pub = generate_rsa_key_pair()
        >>> sig = rsa_sign("hello", priv)
        >>> rsa_verify("hello", sig, pub)
        True
        >>> rsa_verify("tampered", sig, pub)
        False
    """
    if isinstance(message, str):
        message = message.encode("utf-8")
    if algorithm is None:
        algorithm = hashes.SHA256()

    try:
        public_key.verify(
            signature,
            message,
            PSS(
                mgf=MGF1(algorithm),
                salt_length=PSS.MAX_LENGTH,
            ),
            algorithm,
        )
        return True
    except Exception:
        return False
