def tabulate_well_formedness_violations_in_expr(expr):
    r'''.. versionadded:: 1.1

    Tabulate well-formedness violations in `expr`::

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

    ::

        abjad> componenttools.tabulate_well_formedness_violations_in_expr(staff)
        1 /  4 beamed quarter note
        0 /  1 discontiguous spanner
        0 /  5 duplicate i d
        0 /  1 empty container
        0 /  0 intermarked hairpin
        0 /  0 misdurated measure
        0 /  0 misfilled measure
        0 /  4 mispitched tie
        0 /  4 misrepresented flag
        0 /  5 missing parent
        0 /  0 nested measure
        0 /  0 overlapping beam
        0 /  0 overlapping glissando
        0 /  0 overlapping octavation
        0 /  0 short hairpin

    Beamed quarter notes are not well formed.
    '''
    from abjad import checks as _checks

    for key, value in sorted(vars(_checks).items()):
        checker = value()
        checker.report(expr)
