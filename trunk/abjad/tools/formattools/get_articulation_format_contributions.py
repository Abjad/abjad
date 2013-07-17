def get_articulation_format_contributions(component):
    '''.. versionadded:: 2.0

    Get articulation format contributions for `component`.

    Return list.
    '''
    from abjad.tools import marktools

    result = []
    articulations = component.get_marks(marktools.Articulation)
    for articulation in articulations:
        result.append(articulation.lilypond_format)
    result.sort()
    return ['articulations', result]
