# -*- encoding: utf-8 -*-


def get_articulation_format_contributions(component):
    '''Get articulation format contributions for `component`.

    Returns list.
    '''
    from abjad.tools import marktools

    result = []
    articulations = component._get_marks(marktools.Articulation)
    for articulation in articulations:
        result.append(articulation.lilypond_format)
    result.sort()
    return ['articulations', result]
