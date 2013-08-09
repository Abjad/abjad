# -*- encoding: utf-8 -*-


def more(component):
    r'''Gives access to additional component methods.

    Returns extended component interface.
    '''
    from abjad.tools import selectiontools
    return selectiontools.Inspector(component)
