# -*- encoding: utf-8 -*-
from abjad.tools.functiontools import override


def get_grob_override_format_contributions(component):
    r'''Get grob override format contributions for `component`.

    Returns alphabetized list of LilyPond grob overrides.
    '''
    from abjad.tools.scoretools.Leaf import Leaf

    result = []
    if isinstance(component, Leaf):
        is_once = True
    else:
        is_once = False
    result.extend(override(component)._list_format_contributions('override', is_once=is_once))
    for string in result[:]:
        if 'NoteHead' in string and 'pitch' in string:
            result.remove(string)
    result = ['grob overrides', result]
    return result
