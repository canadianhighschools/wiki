import importlib.util
import sys

# taken from https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
def lazy_import(name, package=None):
    spec = importlib.util.find_spec(name, package=package)
    module = importlib.util.module_from_spec(spec)

    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module