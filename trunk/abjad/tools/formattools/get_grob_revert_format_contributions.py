# -*- encoding: utf-8 -*-
from abjad.tools.functiontools import override


def get_grob_revert_format_contributions(component):
    '''Get grob revert format contributions.

    Returns alphabetized list of LilyPond grob reverts.
    '''
    from abjad.tools.scoretools.Leaf import Leaf

    result = []
    if not isinstance(component, Leaf):
        result.extend(override(component)._list_format_contributions('revert'))
    return ['grob reverts', result]
