# -*- encoding: utf-8 -*-


def list_all_abjadide_classes(modules=None):
    r'''Lists all public classes defined in Abjad.

    ::

        >>> all_classes = documentationtools.list_all_abjadide_classes()  # doctest: +SKIP

    '''
    from abjad.tools import documentationtools
    return documentationtools.list_all_classes('abjadide')