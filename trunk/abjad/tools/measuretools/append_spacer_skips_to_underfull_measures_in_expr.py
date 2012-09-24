def append_spacer_skips_to_underfull_measures_in_expr(expr):
    r'''.. versionadded:: 1.1

    Append spacer skips to underfull measures in `expr`::

        >>> staff = Staff(Measure((3, 8), "c'8 d'8 e'8") * 3)
        >>> contexttools.detach_time_signature_marks_attached_to_component(staff[1])
        (TimeSignatureMark((3, 8)),)
        >>> contexttools.TimeSignatureMark((4, 8))(staff[1])
        TimeSignatureMark((4, 8))(|4/8, c'8, d'8, e'8|)
        >>> contexttools.detach_time_signature_marks_attached_to_component(staff[2])
        (TimeSignatureMark((3, 8)),)
        >>> contexttools.TimeSignatureMark((5, 8))(staff[2])
        TimeSignatureMark((5, 8))(|5/8, c'8, d'8, e'8|)
        >>> staff[1].is_underfull
        True
        >>> staff[2].is_underfull
        True

    ::

        >>> measuretools.append_spacer_skips_to_underfull_measures_in_expr(staff)
        [Measure(4/8, [c'8, d'8, e'8, s1 * 1/8]), Measure(5/8, [c'8, d'8, e'8, s1 * 1/4])]

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 3/8
                c'8
                d'8
                e'8
            }
            {
                \time 4/8
                c'8
                d'8
                e'8
                s1 * 1/8
            }
            {
                \time 5/8
                c'8
                d'8
                e'8
                s1 * 1/4
            }
        }

    Return measures treated.

    .. versionchanged:: 2.0
        renamed ``measuretools.remedy_underfull_measures()`` to
        ``measuretools.append_spacer_skips_to_underfull_measures_in_expr()``.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import measuretools

    treated_measures = []
    for rigid_measure in iterationtools.iterate_components_in_expr(expr, measuretools.Measure):
        if rigid_measure.is_underfull:
            measuretools.append_spacer_skip_to_underfull_measure(rigid_measure)
            treated_measures.append(rigid_measure)

    return treated_measures
