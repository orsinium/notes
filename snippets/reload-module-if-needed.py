import os.path
from importlib import reload
from types import ModuleType


def check_module_is_actual(module: ModuleType) -> bool:
    cached_at = os.path.getmtime(module.__cached__)
    modified_at = os.path.getmtime(module.__file__)
    return cached_at >= modified_at


def reload_module(module: ModuleType) -> bool:
    is_actual = check_module_is_actual(module)
    if not is_actual:
        reload(module)
    return is_actual
