# -*- encoding: utf-8 -*-
from abjad.tools import skiptools


def append_spacer_skip_to_underfull_measure(measure):
    r'''Append spacer skip to underfull `measure`:

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

    ..  doctest::

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

    assert isinstance(measure, measuretools.Measure)

    if measure.is_underfull:
        target_duration = measure.time_signature.duration
        duration = measure._get_duration()
        skip = skiptools.Skip((1, 1))
        time_signature_multiplier = \
            measure.time_signature.implied_prolation
        new_multiplier = (target_duration - duration) / time_signature_multiplier
        skip.lilypond_duration_multiplier = new_multiplier
        measure.append(skip)

    return measure
