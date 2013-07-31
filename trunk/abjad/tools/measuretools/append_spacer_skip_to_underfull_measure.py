# -*- encoding: utf-8 -*-
from abjad.tools import skiptools


def append_spacer_skip_to_underfull_measure(rigid_measure):
    r'''.. versionadded:: 1.1

    Append spacer skip to underfull `measure`:

    ::

        >>> measure = Measure((4, 12), "c'8 d'8 e'8 f'8")
        >>> measure.select().detach_marks(contexttools.TimeSignatureMark)
        (TimeSignatureMark((4, 12)),)
        >>> contexttools.TimeSignatureMark((5, 12))(measure)
        TimeSignatureMark((5, 12))(|5/12 c'8 d'8 e'8 f'8|)
        >>> measure.is_underfull
        True

    ::

        >>> measuretools.append_spacer_skip_to_underfull_measure(measure)
        Measure(5/12, [c'8, d'8, e'8, f'8, s1 * 1/8])

    ::

        >>> f(measure)
        {
            \time 5/12
            \scaleDurations #'(2 . 3) {
                c'8
                d'8
                e'8
                f'8
                s1 * 1/8
            }
        }

    Append nothing to nonunderfull `measure`.

    Return `measure`.
    '''
    from abjad.tools import contexttools
    from abjad.tools import measuretools

    assert isinstance(rigid_measure, measuretools.Measure)

    if rigid_measure.is_underfull:
        target_duration = rigid_measure.get_effective_context_mark(
            contexttools.TimeSignatureMark).duration
        duration = rigid_measure.duration
        skip = skiptools.Skip((1, 1))
        time_signature_multiplier = rigid_measure.get_effective_context_mark(
            contexttools.TimeSignatureMark).implied_prolation
        new_multiplier = (target_duration - duration) / time_signature_multiplier
        skip.duration_multiplier = new_multiplier
        rigid_measure.append(skip)

    return rigid_measure
