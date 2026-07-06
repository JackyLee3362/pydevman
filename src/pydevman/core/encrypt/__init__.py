"""
加密/解密、哈希工具模块
========================
提供常用的加密解密函数，按功能分为以下子模块：

- hash.py       哈希/摘要算法（MD5、SHA、BLAKE2、HMAC）
- symmetric.py  对称加密（AES-CBC、AES-GCM）
- asymmetric.py 非对称加密（RSA 加解密、签名验签）
- utils.py      工具函数（随机密钥生成、PBKDF2 密钥派生）

编解码函数已移至独立的 ``pydevman.core.encoding`` 模块，
但为兼容性仍可从本模块导入。
"""

# ---- 哈希 ----
from pydevman.core.encrypt.hash import (
    blake2b,
    file_md5,
    file_sha256,
    hmac_sha256,
    hmac_sha512,
    md5,
    sha1,
    sha256,
    sha512,
    sha256_digest,
)

# ---- 编解码（从 core.encoding 重新导出，保持兼容） ----
from pydevman.core.encoding import (
    base32_decode,
    base32_encode,
    base64_decode,
    base64_decode_bytes,
    base64_encode,
    hex_decode,
    hex_decode_str,
    hex_encode,
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)

# ---- 对称加密 ----
from pydevman.core.encrypt.symmetric import (
    aes_cbc_decrypt,
    aes_cbc_encrypt,
    aes_gcm_decrypt,
    aes_gcm_encrypt,
)

# ---- 非对称加密 ----
from pydevman.core.encrypt.asymmetric import (
    generate_rsa_key_pair,
    load_private_key_from_pem,
    load_public_key_from_pem,
    private_key_to_pem,
    public_key_to_pem,
    rsa_decrypt,
    rsa_encrypt,
    rsa_sign,
    rsa_verify,
)

# ---- 工具 ----
from pydevman.core.encrypt.utils import (
    constant_time_compare,
    derive_key,
    generate_password,
    generate_random_bytes,
    generate_random_key,
    generate_token,
    verify_derived_key,
)

__all__ = [
    # 哈希
    "md5",
    "sha1",
    "sha256",
    "sha512",
    "blake2b",
    "file_md5",
    "file_sha256",
    "hmac_sha256",
    "hmac_sha512",
    "sha256_digest",
    # 编解码
    "base64_encode",
    "base64_decode",
    "base64_decode_bytes",
    "urlsafe_base64_encode",
    "urlsafe_base64_decode",
    "base32_encode",
    "base32_decode",
    "hex_encode",
    "hex_decode",
    "hex_decode_str",
    # 对称加密
    "aes_cbc_encrypt",
    "aes_cbc_decrypt",
    "aes_gcm_encrypt",
    "aes_gcm_decrypt",
    # 非对称加密
    "generate_rsa_key_pair",
    "private_key_to_pem",
    "public_key_to_pem",
    "load_private_key_from_pem",
    "load_public_key_from_pem",
    "rsa_encrypt",
    "rsa_decrypt",
    "rsa_sign",
    "rsa_verify",
    # 工具
    "generate_random_bytes",
    "generate_random_key",
    "generate_token",
    "generate_password",
    "derive_key",
    "verify_derived_key",
    "constant_time_compare",
]
