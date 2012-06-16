def get_articulation_format_contributions(component):
    '''.. versionadded:: 2.0

    Get articulation format contributions for `component`.

    Return list.
    '''
    from abjad.tools import marktools

    result = []
    articulations = marktools.get_articulations_attached_to_component(component)
    for articulation in articulations:
        result.append(articulation.lilypond_format)
    result.sort()
    return ['articulations', result]
