import os


def ensure_file_exists(path: str, default_content: str = "") -> None:
    """
    Ensures that a file exists at the specified path. If the file does not exist, it creates an new file with default content.

    :param path: The path to the file to check or create
    :type path: str
    :param default_content: The content to write to the file if it does not exist, defaults to an empty string
    :type default_content: str, optional
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(default_content)
