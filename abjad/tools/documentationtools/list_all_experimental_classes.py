# -*- coding: utf-8 -*-


def list_all_experimental_classes(modules=None, ignored_classes=None):
    r'''Lists all public classes defined in the Abjad experimental branch.

    ::

        >>> all_classes = documentationtools.list_all_experimental_classes()  # doctest: +SKIP

    '''
    from abjad.tools import documentationtools
    try:
        return documentationtools.list_all_classes(
            modules='experimental',
            ignored_classes=ignored_classes,
            )
    except ImportError:
        return []
