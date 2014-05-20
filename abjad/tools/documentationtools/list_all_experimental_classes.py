# -*- encoding: utf-8 -*-
import collections
import types


def list_all_experimental_classes(modules=None):
    r'''Lists all public classes defined in the Abjad experimental branch.

    ::

        >>> all_classes = documentationtools.list_all_experimental_classes()

    '''
    from abjad import abjad_configuration
    from abjad.tools import documentationtools
    all_classes = set()
    paths = []
    if modules is None:
        paths.append(abjad_configuration.abjad_experimental_directory)
    elif isinstance(modules, types.ModuleType):
        paths.extend(modules.__path__)
    elif isinstance(modules, collections.Iterable):
        for module in modules:
            if isinstance(module, types.ModuleType):
                paths.extend(module.__path__)
    for path in paths:
        class_documenter = documentationtools.ClassCrawler(path)
        for x in class_documenter():
            all_classes.add(x)
    return list(all_classes)