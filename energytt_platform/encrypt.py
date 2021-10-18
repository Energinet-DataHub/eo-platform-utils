# AES 256 encryption/decryption using pycrypto library

import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

_BLOCK_SIZE = 16
# _pad = lambda s: s + (_BLOCK_SIZE - len(s) % _BLOCK_SIZE) * chr(_BLOCK_SIZE - len(s) % _BLOCK_SIZE)
# _unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def _pad(s: str) -> str:
    return (s + (_BLOCK_SIZE - len(s) % _BLOCK_SIZE)
            * chr(_BLOCK_SIZE - len(s) % _BLOCK_SIZE))


def _unpad(s: bytes) -> bytes:
    return s[:-ord(s[len(s) - 1:])]


def aes256_encrypt(data: str, key: str) -> str:
    """
    TODO
    """
    private_key = hashlib.sha256(key.encode('utf8')).digest()
    data = _pad(data)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(
        iv + cipher.encrypt(data.encode('utf8'))).decode('utf8')


def aes256_decrypt(data_encrypted: str, key: str) -> str:
    """
    TODO
    """
    data_encrypted = data_encrypted.encode('utf8')
    private_key = hashlib.sha256(key.encode('utf8')).digest()
    data_encrypted = base64.b64decode(data_encrypted)
    iv = data_encrypted[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(data_encrypted[16:])).decode('utf8')
