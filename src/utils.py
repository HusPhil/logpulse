import os


def get_files_in_dir(directory: str, extensions=None) -> list[str]:
    """
    Return list of files in `directory`.
    If `extensions` is provided, only return matching ones.
    Example: extensions=[".txt", ".log"]
    """
    if not os.path.isdir(directory):
        return []

    files = []
    for f in os.listdir(directory):
        full_path = os.path.join(directory, f)
        if os.path.isfile(full_path):
            if extensions:
                if any(f.lower().endswith(ext.lower()) for ext in extensions):
                    files.append(f)
            else:
                files.append(f)
    return files
