# -*- encoding: utf-8 -*-
from abjad.tools.topleveltools import iterate


def append_spacer_skips_to_underfull_measures_in_expr(expr):
    r'''Append spacer skips to underfull measures in `expr`:

    ::

        >>> staff = Staff(Measure((3, 8), "c'8 d'8 e'8") * 3)
        >>> time_signature = inspect(staff[1]).get_mark(
        ...     marktools.TimeSignature)
        >>> time_signature.detach()
        TimeSignature((3, 8))
        >>> new_time_signature = marktools.TimeSignature((4, 8))
        >>> attach(new_time_signature, staff[1])
        TimeSignature((4, 8))(|4/8 c'8 d'8 e'8|)
        >>> time_signature = inspect(
        ...     staff[2]).get_mark(marktools.TimeSignature)
        >>> time_signature.detach()
        TimeSignature((3, 8))
        >>> new_time_signature = marktools.TimeSignature((5, 8))
        >>> attach(new_time_signature, staff[2])
        TimeSignature((5, 8))(|5/8 c'8 d'8 e'8|)
        >>> staff[1].is_underfull
        True
        >>> staff[2].is_underfull
        True

    ::

        >>> scoretools.append_spacer_skips_to_underfull_measures_in_expr(staff)
        [Measure(4/8, [c'8, d'8, e'8, s1 * 1/8]), Measure(5/8, [c'8, d'8, e'8, s1 * 1/4])]

    ..  doctest::

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

    Returns measures treated.
    '''
    from abjad.tools import scoretools

    treated_measures = []
    for measure in iterate(expr).by_class(scoretools.Measure):
        if measure.is_underfull:
            scoretools.append_spacer_skip_to_underfull_measure(measure)
            treated_measures.append(measure)

    return treated_measures
