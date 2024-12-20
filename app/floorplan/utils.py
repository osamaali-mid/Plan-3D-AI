import os

def create_directory(path):
    """
    Create a directory if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)
