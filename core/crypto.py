import ctypes
import ctypes.wintypes
import json

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD),
                ("pbData", ctypes.POINTER(ctypes.c_byte))]

crypt32 = ctypes.windll.crypt32

def encrypt_data(data_dict: dict) -> bytes:
    """
    Encrypts a dictionary to bytes using Windows DPAPI via ctypes.
    """
    json_bytes = json.dumps(data_dict).encode('utf-8')
    
    # We need to create a mutable string buffer to cast to pointer
    data_buffer = ctypes.create_string_buffer(json_bytes)
    data_in = DATA_BLOB(len(json_bytes), ctypes.cast(data_buffer, ctypes.POINTER(ctypes.c_byte)))
    data_out = DATA_BLOB()
    
    # CryptProtectData
    if crypt32.CryptProtectData(ctypes.byref(data_in), "RunAsConfig", None, None, None, 0, ctypes.byref(data_out)):
        res = ctypes.string_at(data_out.pbData, data_out.cbData)
        ctypes.windll.kernel32.LocalFree(data_out.pbData)
        return res
    else:
        raise Exception("CryptProtectData failed")

def decrypt_data(encrypted_bytes: bytes) -> dict:
    """
    Decrypts bytes back to a dictionary using Windows DPAPI via ctypes.
    """
    data_buffer = ctypes.create_string_buffer(encrypted_bytes)
    data_in = DATA_BLOB(len(encrypted_bytes), ctypes.cast(data_buffer, ctypes.POINTER(ctypes.c_byte)))
    data_out = DATA_BLOB()
    
    if crypt32.CryptUnprotectData(ctypes.byref(data_in), None, None, None, None, 0, ctypes.byref(data_out)):
        res = ctypes.string_at(data_out.pbData, data_out.cbData)
        ctypes.windll.kernel32.LocalFree(data_out.pbData)
        return json.loads(res.decode('utf-8'))
    else:
        raise Exception("CryptUnprotectData failed")
