# -*- coding: utf-8 -*-
import collections
import importlib
import types


def list_all_classes(modules=None, ignored_classes=None):
    r'''Lists all public classes defined in `path`.

    ::

        >>> all_classes = documentationtools.list_all_classes(
        ...     modules='abjad',
        ...     )

    '''
    from abjad import abjad_configuration
    from abjad.tools import documentationtools
    all_classes = set()
    paths = []
    if modules is None:
        paths.append(abjad_configuration.abjad_directory)
    elif isinstance(modules, str):
        module = importlib.import_module(modules)
        paths.extend(module.__path__)
    elif isinstance(modules, types.ModuleType):
        paths.extend(modules.__path__)
    elif isinstance(modules, collections.Iterable):
        for module in modules:
            if isinstance(module, types.ModuleType):
                paths.extend(module.__path__)
            elif isinstance(module, str):
                module = importlib.import_module(module)
                paths.extend(module.__path__)
            else:
                raise ValueError(module)
    else:
        raise ValueError(modules)
    for path in paths:
        for x in documentationtools.yield_all_classes(code_root=path):
            all_classes.add(x)
    if ignored_classes:
        ignored_classes = set(ignored_classes)
        all_classes.difference_update(ignored_classes)
    return list(sorted(
        all_classes,
        key=lambda x: (x.__module__, x.__name__)
        ))
