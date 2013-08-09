# -*- encoding: utf-8 -*-
from abjad.tools.selectiontools import more


def get_articulation_format_contributions(component):
    '''Get articulation format contributions for `component`.

    Return list.
    '''
    from abjad.tools import marktools

    result = []
    articulations = component._get_marks(marktools.Articulation)
    for articulation in articulations:
        result.append(articulation.lilypond_format)
    result.sort()
    return ['articulations', result]
