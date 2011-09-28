def list_badly_formed_components_in_expr(expr, allow_empty_containers=True):
    r'''.. versionadded:: 1.1

    List badly formed components in `expr`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> staff[1].written_duration = Duration(1, 4)
        abjad> spannertools.BeamSpanner(staff[:])
        BeamSpanner(c'8, d'4, e'8, f'8)
        abjad> f(staff)
        \new Staff {
            c'8 [
            d'4
            e'8
            f'8 ]
        }
        abjad> componenttools.list_badly_formed_components_in_expr(staff)
        [Note("d'4")]

    Beamed quarter notes are not well formed.

    Return newly created list of zero or more components.
    '''
    from abjad import checks as _checks

    badly_formed_components = []
    for key, value in sorted(vars(_checks).items()):
        checker = value()
        badly_formed_components.extend(checker.violators(expr))
    return badly_formed_components
