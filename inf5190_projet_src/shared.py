import os


def get_path(file):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(BASE_DIR, file)
