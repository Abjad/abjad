# -*- coding: utf-8 -*-


def list_all_ide_functions(modules=None):
    r'''Lists all public functions defined in Abjad IDE.

    ::

        >>> all_functions = documentationtools.list_all_ide_functions()  # doctest: +SKIP

    '''
    from abjad.tools import documentationtools
    try:
        return documentationtools.list_all_functions(modules='ide')
    except ImportError:
        return []
