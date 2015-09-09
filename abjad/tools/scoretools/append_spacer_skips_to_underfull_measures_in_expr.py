# -*- coding: utf-8 -*-
from abjad.tools.topleveltools import iterate


def append_spacer_skips_to_underfull_measures_in_expr(expr):
    r'''Append spacer skips to underfull measures in `expr`:

    ::

        >>> staff = Staff(Measure((3, 8), "c'8 d'8 e'8") * 3)
        >>> detach(TimeSignature, staff[1])
        (TimeSignature((3, 8)),)
        >>> new_time_signature = TimeSignature((4, 8))
        >>> attach(new_time_signature, staff[1])
        >>> detach(TimeSignature, staff[2])
        (TimeSignature((3, 8)),)
        >>> new_time_signature = TimeSignature((5, 8))
        >>> attach(new_time_signature, staff[2])
        >>> staff[1].is_underfull
        True
        >>> staff[2].is_underfull
        True

    ::

        >>> scoretools.append_spacer_skips_to_underfull_measures_in_expr(staff)
        [Measure((4, 8), "c'8 d'8 e'8 s1 * 1/8"), Measure((5, 8), "c'8 d'8 e'8 s1 * 1/4")]

    ..  doctest::

        >>> print(format(staff))
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

    Returns measures treated.
    '''
    from abjad.tools import scoretools

    treated_measures = []
    for measure in iterate(expr).by_class(scoretools.Measure):
        if measure.is_underfull:
            scoretools.append_spacer_skip_to_underfull_measure(measure)
            treated_measures.append(measure)

    return treated_measures
