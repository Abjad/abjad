# -*- encoding: utf-8 -*-


def list_all_experimental_classes(modules=None):
    r'''Lists all public classes defined in the Abjad experimental branch.

    ::

        >>> all_classes = documentationtools.list_all_experimental_classes()

    '''
    from abjad.tools import documentationtools
    return documentationtools.list_all_classes('experimental')