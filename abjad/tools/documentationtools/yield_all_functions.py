import types


def yield_all_functions(
    code_root=None,
    include_private_objects=False,
    root_package_name=None,
    ):
    r'''Yields all functions in `code_root`.

    Returns generator.
    '''
    from abjad.tools import documentationtools
    for module in documentationtools.yield_all_modules(
        code_root=code_root,
        root_package_name=root_package_name,
        ):
        name = module.__name__.split('.')[-1]
        if not include_private_objects and name.startswith('_'):
            continue
        if not hasattr(module, name):
            continue
        obj = getattr(module, name)
        if isinstance(obj, types.FunctionType):
            yield obj
