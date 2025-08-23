from pathlib import Path



def create_file_if_not_exists(file_path: str) -> None:
    """
    Creates a file if it does not already exist. If the file's parent directories 
    don't exist, they will be created as well.

    Args:
        file_path (str): Path to the file to be created.
    """
    try:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.is_file():
            file_path.touch()               
    except Exception:
        raise Exception(f"Failed to create file at {file_path}")