def _get_stem_tremolo_format_contributions(component):
    '''.. versionadded:: 2.0
    '''
    from abjad.tools import marktools

    result = []

#    stem_tremolos = marktools.get_stem_tremolo_attached_to_component(component)
#    for stem_tremolo in stem_tremolos:
#        result.append(stem_tremolo.format)
#    result.sort()

    if marktools.is_component_with_stem_tremolo_attached(component):
        stem_tremolo = marktools.get_stem_tremolo_attached_to_component(component)
        result.append(stem_tremolo.format)

    return ['stem tremolo', result]
