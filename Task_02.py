import ctypes
from ctypes import wintypes, byref
import time

def unbuffered_file_read(file_path):
    GENERIC_READ = 0x80000000
    OPEN_EXISTING = 0x3
    FILE_FLAG_NO_BUFFERING = 0x20000000

    start_time = time.time()
    handle = ctypes.windll.kernel32.CreateFileW(
        file_path, GENERIC_READ, 0, None, OPEN_EXISTING, FILE_FLAG_NO_BUFFERING, None
    )

    if handle == -1:
        raise Exception("Failed to open file.")

    buffer = ctypes.create_string_buffer(4096)  # 4KB блок
    bytes_read = wintypes.DWORD()

    while True:
        success = ctypes.windll.kernel32.ReadFile(
            handle, buffer, len(buffer), byref(bytes_read), None
        )
        if not success or bytes_read.value == 0:
            break

    ctypes.windll.kernel32.CloseHandle(handle)
    end_time = time.time()
    print(f"Unbuffered read completed in {end_time - start_time:.4f} seconds.")

if __name__ == "__main__":
    file_path = r"C:\path\to\large_file.dat"
    unbuffered_file_read(file_path)
