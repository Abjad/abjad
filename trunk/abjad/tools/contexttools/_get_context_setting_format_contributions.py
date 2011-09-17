def _get_context_setting_format_contributions(component):
    '''Sorted list of format-time context settings.
    '''
    result = []
    from abjad.tools.leaftools._Leaf import _Leaf
    from abjad.tools.measuretools.Measure import Measure
    from abjad.tools.lilypondfiletools._format_lilypond_context_setting_inline import _format_lilypond_context_setting_inline
    from abjad.tools.lilypondfiletools._format_lilypond_context_setting_in_with_block import _format_lilypond_context_setting_in_with_block
    if isinstance(component, (_Leaf, Measure)):
        for name, value in vars(component.set).iteritems():
            # if we've found a leaf LilyPondContextNamespace
            if name.startswith('_'):
                # parse all the public names in the LilyPondContextNamespace
                for x, y in vars(value).iteritems():
                    if not x.startswith('_'):
                        result.append(_format_lilypond_context_setting_inline(x, y, name))
            # otherwise we've found a default leaf context setting
            else:
                # parse default context setting
                result.append(_format_lilypond_context_setting_inline(name, value))
    else:
        for name, value in vars(component.set).iteritems():
            result.append(_format_lilypond_context_setting_in_with_block(name, value))
    result.sort()
    return ['context settings', result]
