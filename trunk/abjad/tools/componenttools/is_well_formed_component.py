from abjad.tools.componenttools._Component import _Component


def is_well_formed_component(expr, allow_empty_containers=True):
    r'''.. versionadded:: 1.1

    True when `component` is well formed::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> spannertools.BeamSpanner(staff[:])
        BeamSpanner(c'8, d'8, e'8, f'8)
        abjad> componenttools.is_well_formed_component(staff)
        True

    Otherwise false::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> staff[1].written_duration = Duration(1, 4)
        abjad> spannertools.BeamSpanner(staff[:])
        BeamSpanner(c'8, d'4, e'8, f'8)
        abjad> componenttools.is_well_formed_component(staff)
        False

    Beamed quarter notes are not well formed.

    Return boolean.
    '''
    from abjad import checks as _checks

    if not isinstance(expr, _Component):
        return False

    results = []
    for key, value in sorted(vars(_checks).items()):
        checker = value()
        if allow_empty_containers:
            if getattr(checker, 'runtime', False) == 'composition':
                continue
        results.append(checker.check(expr))
        #print results
    return all(results)
