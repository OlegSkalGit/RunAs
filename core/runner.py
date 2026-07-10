import ctypes
import ctypes.wintypes
import os

advapi32 = ctypes.windll.advapi32
kernel32 = ctypes.windll.kernel32

LOGON_WITH_PROFILE = 1
CREATE_NEW_CONSOLE = 0x00000010
CREATE_UNICODE_ENVIRONMENT = 0x00000400
STARTF_USESHOWWINDOW = 0x00000001
SW_HIDE = 0

class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb", ctypes.wintypes.DWORD),
        ("lpReserved", ctypes.wintypes.LPWSTR),
        ("lpDesktop", ctypes.wintypes.LPWSTR),
        ("lpTitle", ctypes.wintypes.LPWSTR),
        ("dwX", ctypes.wintypes.DWORD),
        ("dwY", ctypes.wintypes.DWORD),
        ("dwXSize", ctypes.wintypes.DWORD),
        ("dwYSize", ctypes.wintypes.DWORD),
        ("dwXCountChars", ctypes.wintypes.DWORD),
        ("dwYCountChars", ctypes.wintypes.DWORD),
        ("dwFillAttribute", ctypes.wintypes.DWORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("wShowWindow", ctypes.wintypes.WORD),
        ("cbReserved2", ctypes.wintypes.WORD),
        ("lpReserved2", ctypes.POINTER(ctypes.c_byte)),
        ("hStdInput", ctypes.wintypes.HANDLE),
        ("hStdOutput", ctypes.wintypes.HANDLE),
        ("hStdError", ctypes.wintypes.HANDLE),
    ]

class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", ctypes.wintypes.HANDLE),
        ("hThread", ctypes.wintypes.HANDLE),
        ("dwProcessId", ctypes.wintypes.DWORD),
        ("dwThreadId", ctypes.wintypes.DWORD),
    ]

def run_commands_as_user(username, password, domain, commands, wait_for_completion=True):
    if not domain:
        domain = "."
    results = []
    
    for cmd in commands:
        if not cmd.strip():
            continue
            
        try:
            command_line = cmd
            
            si = STARTUPINFO()
            si.cb = ctypes.sizeof(STARTUPINFO)
            si.dwFlags = STARTF_USESHOWWINDOW
            si.wShowWindow = 5  # SW_SHOW
            
            pi = PROCESS_INFORMATION()
            
            creation_flags = CREATE_NEW_CONSOLE | CREATE_UNICODE_ENVIRONMENT
            
            res = advapi32.CreateProcessWithLogonW(
                ctypes.c_wchar_p(username),
                ctypes.c_wchar_p(domain),
                ctypes.c_wchar_p(password),
                LOGON_WITH_PROFILE,
                None,
                ctypes.create_unicode_buffer(command_line),
                creation_flags,
                None,
                ctypes.c_wchar_p(os.getcwd()),
                ctypes.byref(si),
                ctypes.byref(pi)
            )
            
            if res:
                if wait_for_completion:
                    kernel32.WaitForSingleObject(pi.hProcess, 0xFFFFFFFF) # INFINITE
                    exit_code = ctypes.wintypes.DWORD()
                    kernel32.GetExitCodeProcess(pi.hProcess, ctypes.byref(exit_code))
                    status_msg = "Success" if exit_code.value == 0 else f"Failed (exit code {exit_code.value})"
                    code_val = exit_code.value
                else:
                    status_msg = "Success (Launched asynchronously)"
                    code_val = 0
                    
                kernel32.CloseHandle(pi.hProcess)
                kernel32.CloseHandle(pi.hThread)
                
                results.append({
                    "command": cmd, 
                    "status": status_msg, 
                    "exit_code": code_val
                })
            else:
                err = kernel32.GetLastError()
                results.append({
                    "command": cmd, 
                    "status": f"CreateProcessWithLogonW failed with error {err}", 
                    "exit_code": -1
                })
                
        except Exception as e:
            results.append({
                "command": cmd, 
                "status": f"Error: {str(e)}", 
                "exit_code": -1
            })
            
    return results
