import ctypes
from ctypes import wintypes, byref
import time

def async_file_read(file_path):
    GENERIC_READ = 0x80000000
    FILE_FLAG_OVERLAPPED = 0x40000000
    OPEN_EXISTING = 0x3

    overlapped = wintypes.OVERLAPPED()
    buffer = ctypes.create_string_buffer(4096)  # 4KB блок
    bytes_read = wintypes.DWORD()

    handle = ctypes.windll.kernel32.CreateFileW(
        file_path, GENERIC_READ, 0, None, OPEN_EXISTING, FILE_FLAG_OVERLAPPED, None
    )

    if handle == -1:
        raise Exception("Failed to open file.")

    start_time = time.time()
    success = ctypes.windll.kernel32.ReadFile(
        handle, buffer, len(buffer), byref(bytes_read), byref(overlapped)
    )

    # Очікуємо завершення асинхронного читання
    if not success:
        ctypes.windll.kernel32.GetOverlappedResult(handle, byref(overlapped), byref(bytes_read), True)

    ctypes.windll.kernel32.CloseHandle(handle)
    end_time = time.time()
    print(f"Asynchronous read completed in {end_time - start_time:.4f} seconds.")

if __name__ == "__main__":
    file_path = r"C:\path\to\large_file.dat"
    async_file_read(file_path)
