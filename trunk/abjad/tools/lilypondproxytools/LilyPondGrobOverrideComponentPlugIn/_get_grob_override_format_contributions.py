def _get_grob_override_format_contributions(component):
    '''Alphabetized list of LilyPond grob overrides.
    '''
    from abjad.tools.leaftools._Leaf import _Leaf

    result = []
    if isinstance(component, _Leaf):
        is_once = True
    else:
        is_once = False
    result.extend(component.override._list_format_contributions('override', is_once = is_once))
    for override in result[:]:
        if 'NoteHead' in override and 'pitch' in override:
            result.remove(override)
    result = ['grob overrides', result]
    return result
