import os


def ensure_file_exists(path: str) -> None:
    """
    Ensures that a file exists at the specified path. If the file does not exist, it creates an empty file.

    :param path: The path to the file to check or create
    :type path: str
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("")
