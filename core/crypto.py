import json
import base64
import os
import hashlib
import struct

def _derive_key(password: str, salt: bytes) -> bytes:
    """
    Derives a 32-byte symmetric key from the given password and salt using PBKDF2.
    """
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, 32)

def _stream_cipher(data: bytes, key: bytes, nonce: bytes) -> bytes:
    """
    A simple CTR-like stream cipher using SHA-256 to generate a keystream.
    This provides AES-like symmetric encryption using only the standard library.
    """
    out = bytearray()
    counter = 0
    # Generate keystream blocks until we have enough to XOR the data
    while len(out) < len(data):
        # Pack the counter as an 8-byte little-endian unsigned long long
        block_data = nonce + struct.pack('<Q', counter)
        keystream_block = hashlib.sha256(key + block_data).digest()
        out.extend(keystream_block)
        counter += 1
    
    # XOR data with keystream
    return bytes(a ^ b for a, b in zip(data, out[:len(data)]))

def encrypt_data(data_dict: dict, password: str) -> bytes:
    """
    Encrypts a dictionary to base64 bytes using a custom stream cipher derived from a password.
    Format: Base64( Salt (16 bytes) + Nonce (16 bytes) + Ciphertext )
    """
    json_bytes = json.dumps(data_dict).encode('utf-8')
    salt = os.urandom(16)
    nonce = os.urandom(16)
    key = _derive_key(password, salt)
    
    encrypted = _stream_cipher(json_bytes, key, nonce)
    return base64.b64encode(salt + nonce + encrypted)

def decrypt_data(encrypted_bytes: bytes, password: str) -> dict:
    """
    Decrypts base64 bytes back to a dictionary using the provided password.
    """
    try:
        raw = base64.b64decode(encrypted_bytes)
        if len(raw) < 32:
            raise ValueError("Invalid encrypted data length")
            
        salt = raw[:16]
        nonce = raw[16:32]
        encrypted = raw[32:]
        
        key = _derive_key(password, salt)
        decrypted_bytes = _stream_cipher(encrypted, key, nonce)
        
        return json.loads(decrypted_bytes.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ValueError("Невірний пароль для розшифрування або пошкоджений файл.")
    except Exception as e:
        raise Exception(f"Помилка розшифрування конфігурації: {e}")
