import importlib.util
import sys

# taken from https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
def lazy_import(name):
    spec = importlib.util.find_spec(name)
    loader = importlib.util.LazyLoader(spec.loader)

    spec.loader = loader
    module = importlib.util.module_from_spec(spec)

    sys.modules[name] = module
    loader.exec_module(module)
    return module