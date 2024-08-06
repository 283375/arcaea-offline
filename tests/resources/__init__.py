import importlib.resources
import sys


def get_resource(path: str):
    """
    A wrapper for `importlib.resources.files()` since it's not available in Python 3.8.
    """
    if sys.version_info >= (3, 9, 0):
        with importlib.resources.as_file(
            importlib.resources.files(__name__).joinpath(path)
        ) as resource_path:
            return resource_path

    with importlib.resources.path(__name__, path) as resource_path:
        return resource_path
