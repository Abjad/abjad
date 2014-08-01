# -*- encoding: utf-8 -*-
import collections
import types


def list_all_abjad_classes(modules=None):
    r'''Lists all public classes defined in Abjad.

    ::

        >>> all_classes = documentationtools.list_all_abjad_classes()

    '''
    from abjad.tools import documentationtools
    return documentationtools.list_all_classes('abjad')