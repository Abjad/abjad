# -*- coding: utf-8 -*-


def list_all_ide_classes(modules=None, ignored_classes=None):
    r'''Lists all public classes defined in Abjad IDE.

    ::

        >>> all_classes = documentationtools.list_all_ide_classes()  # doctest: +SKIP

    '''
    from abjad.tools import documentationtools
    try:
        return documentationtools.list_all_classes(
            modules='ide',
            ignored_classes=ignored_classes,
            )
    except ImportError:
        return []
