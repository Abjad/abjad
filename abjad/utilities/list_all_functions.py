import types


def list_all_functions(modules=None):
    r'''Lists all public functions defined in `modules`.

    ..  container:: example

        ::

            >>> all_functions = abjad.utilities.list_all_functions(
            ...     modules='abjad',
            ...     )

    '''
    from abjad import utilities
    all_functions = set()
    for module in utilities.yield_all_modules(modules):
        name = module.__name__.split('.')[-1]
        if name.startswith('_'):
            continue
        if not hasattr(module, name):
            continue
        obj = getattr(module, name)
        if isinstance(obj, types.FunctionType):
            all_functions.add(obj)
    return list(sorted(
        all_functions,
        key=lambda x: (x.__module__, x.__name__)
        ))
