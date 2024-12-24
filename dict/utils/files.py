import os
from logging import error
from typing import List


def list_files_recursively() -> List[str]:
    files: List[str] = []
    for root, dirs, filenames in os.walk("."):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for filename in filenames:
            if not filename.startswith("."):
                full_path = os.path.join(root, filename)
                normalized_path = os.path.relpath(full_path, ".")
                files.append(normalized_path)
    return files


def file_content(filename: str) -> str | None:
    try:
        f = open(filename)
    except FileNotFoundError:
        error(f"Failed to open file {filename}.")
        return None
    try:
        return f.read()
    except Exception as e:
        error(f"Could not read file {filename}: {str(e)}")
        return None
