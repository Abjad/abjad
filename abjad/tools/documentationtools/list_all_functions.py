# -*- coding: utf-8 -*-
import collections
import types


def list_all_functions(modules=None):
    r'''Lists all public functions defined in `modules`.

    ::

        >>> all_functions = documentationtools.list_all_functions(
        ...     modules='abjad',
        ...     )

    '''
    from abjad import abjad_configuration
    from abjad.tools import documentationtools
    all_functions = set()
    paths = []
    if modules is None:
        paths.append(abjad_configuration.abjad_directory)
    elif isinstance(modules, types.ModuleType):
        paths.extend(modules.__path__)
    elif isinstance(modules, collections.Iterable):
        for module in modules:
            if isinstance(module, types.ModuleType):
                paths.extend(module.__path__)
    for path in paths:
        for x in documentationtools.yield_all_classes(code_root=path):
            all_functions.add(x)
    return list(sorted(
        all_functions,
        key=lambda x: (x.__module__, x.__name__)
        ))
