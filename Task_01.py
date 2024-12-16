import os
import ctypes
from ctypes import wintypes, byref
import win32security
import win32api
import pywintypes
import time

# Функція для отримання атрибутів файлу
def get_file_info(file_path):
    INVALID_FILE_ATTRIBUTES = -1

    # Константи атрибутів
    FILE_ATTRIBUTE_READONLY = 0x1
    FILE_ATTRIBUTE_HIDDEN = 0x2
    FILE_ATTRIBUTE_SYSTEM = 0x4

    # Часові структури
    creation_time = wintypes.FILETIME()
    last_access_time = wintypes.FILETIME()
    last_write_time = wintypes.FILETIME()

    # Відкрити файл для читання
    hFile = win32api.CreateFile(file_path, win32api.GENERIC_READ, 0, None,
                                win32api.OPEN_EXISTING, 0, 0)

    # Отримати розмір файлу
    file_size = win32api.GetFileSize(hFile)

    # Отримати часи файлу
    win32api.GetFileTime(hFile, byref(creation_time), byref(last_access_time), byref(last_write_time))

    # Закрити дескриптор файлу
    win32api.CloseHandle(hFile)

    # Отримати атрибути файлу
    attributes = ctypes.windll.kernel32.GetFileAttributesW(file_path)
    if attributes == INVALID_FILE_ATTRIBUTES:
        raise Exception("Failed to get file attributes.")

    print("File Information:")
    print(f"Size: {file_size} bytes")
    print(f"Creation Time: {convert_filetime(creation_time)}")
    print(f"Last Access Time: {convert_filetime(last_access_time)}")
    print(f"Last Write Time: {convert_filetime(last_write_time)}")
    print(f"Attributes: {attributes}")

    # Розшифровка атрибутів
    if attributes & FILE_ATTRIBUTE_READONLY:
        print(" - Read-only")
    if attributes & FILE_ATTRIBUTE_HIDDEN:
        print(" - Hidden")
    if attributes & FILE_ATTRIBUTE_SYSTEM:
        print(" - System File")

# Конвертація FILETIME у зрозумілу дату
def convert_filetime(filetime):
    timestamp = (filetime.dwHighDateTime << 32) + filetime.dwLowDateTime
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp / 10**7 - 11644473600))

if __name__ == "__main__":
    file_path = r"C:\path\to\your\file.txt"  # Шлях до файлу
    get_file_info(file_path)
