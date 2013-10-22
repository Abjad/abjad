# -*- encoding: utf-8 -*-


def get_grob_revert_format_contributions(component):
    '''Get grob revert format contributions.

    Returns alphabetized list of LilyPond grob reverts.
    '''
    from abjad.tools.leaftools.Leaf import Leaf

    result = []
    if not isinstance(component, Leaf):
        result.extend(component.override._list_format_contributions('revert'))
    return ['grob reverts', result]
