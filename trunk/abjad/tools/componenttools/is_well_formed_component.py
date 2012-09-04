def is_well_formed_component(expr, allow_empty_containers=True):
    r'''.. versionadded:: 1.1

    True when `component` is well formed::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beamtools.BeamSpanner(staff[:])
        BeamSpanner(c'8, d'8, e'8, f'8)
        >>> componenttools.is_well_formed_component(staff)
        True

    Otherwise false::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> staff[1].written_duration = Duration(1, 4)
        >>> beamtools.BeamSpanner(staff[:])
        BeamSpanner(c'8, d'4, e'8, f'8)
        >>> componenttools.is_well_formed_component(staff)
        False

    Beamed quarter notes are not well formed.

    Return boolean.
    '''
    from abjad.tools import componenttools
    from abjad.tools import wellformednesstools

    if not isinstance(expr, componenttools.Component):
        return False

    results = []
    for checker in wellformednesstools.list_checks():
        if allow_empty_containers:
            if getattr(checker, 'runtime', False) == 'composition':
                continue
        results.append(checker.check(expr))
    return all(results)
