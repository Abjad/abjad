import types

from .yield_all_modules import yield_all_modules


def list_all_functions(modules=None):
    """
    Lists all public functions defined in `modules`.

    ..  container:: example

        >>> all_functions = abjad.list_all_functions(modules="abjad")

    """
    all_functions = set()
    for module in yield_all_modules(modules):
        name = module.__name__.split(".")[-1]
        if name.startswith("_"):
            continue
        if not hasattr(module, name):
            continue
        obj = getattr(module, name)
        if isinstance(obj, types.FunctionType):
            all_functions.add(obj)
    return list(sorted(all_functions, key=lambda x: (x.__module__, x.__name__)))
