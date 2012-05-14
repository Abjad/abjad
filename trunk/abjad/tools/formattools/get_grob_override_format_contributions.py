def get_grob_override_format_contributions(component):
    r'''.. versionadded:: 2.0

    Get grob override format contributions for `component`.

    Return alphabetized list of LilyPond grob overrides.
    '''
    from abjad.tools.leaftools.Leaf import Leaf

    result = []
    if isinstance(component, Leaf):
        is_once = True
    else:
        is_once = False
    result.extend(component.override._list_format_contributions('override', is_once=is_once))
    for override in result[:]:
        if 'NoteHead' in override and 'pitch' in override:
            result.remove(override)
    result = ['grob overrides', result]
    return result
