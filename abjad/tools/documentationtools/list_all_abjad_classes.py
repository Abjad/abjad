# -*- coding: utf-8 -*-


def list_all_abjad_classes(modules=None, ignored_classes=None):
    r'''Lists all public classes defined in Abjad.

    ::

        >>> all_classes = documentationtools.list_all_abjad_classes()

    '''
    from abjad.tools import documentationtools
    return documentationtools.list_all_classes(
        modules='abjad',
        ignored_classes=ignored_classes,
        )
