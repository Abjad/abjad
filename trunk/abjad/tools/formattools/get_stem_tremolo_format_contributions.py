def get_stem_tremolo_format_contributions(component):
    '''.. versionadded:: 2.0

    Get stem tremolo format contributions for `component`.
       
    Return list.
    '''
    from abjad.tools import marktools

    result = []

    if marktools.is_component_with_stem_tremolo_attached(component):
        stem_tremolo = marktools.get_stem_tremolo_attached_to_component(component)
        result.append(stem_tremolo.lilypond_format)

    return ['stem tremolo', result]
