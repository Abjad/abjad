# -*- coding: utf-8 -*-


def list_all_abjad_functions(modules=None):
    r'''Lists all public functions defined in Abjad.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> all_functions = abjad.documentationtools.list_all_abjad_functions()

    '''
    from abjad.tools import documentationtools
    return documentationtools.list_all_functions(modules='abjad')
