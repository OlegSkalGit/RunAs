import os
from core.crypto import encrypt_data, decrypt_data

def save_config(filepath: str, data: dict, password: str):
    """
    Saves the configuration dictionary to an encrypted file using the provided password.
    """
    encrypted_bytes = encrypt_data(data, password)
    with open(filepath, 'wb') as f:
        f.write(encrypted_bytes)

def load_config(filepath: str, password: str) -> dict:
    """
    Loads and decrypts the configuration dictionary from a file using the provided password.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    with open(filepath, 'rb') as f:
        encrypted_bytes = f.read()
        
    return decrypt_data(encrypted_bytes, password)
