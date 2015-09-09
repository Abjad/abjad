# -*- coding: utf-8 -*-
from abjad.tools.topleveltools import attach


def append_spacer_skip_to_underfull_measure(measure):
    r'''Append spacer skip to underfull `measure`:

    ::

        >>> measure = Measure((4, 12), "c'8 d'8 e'8 f'8")
        >>> measure.implicit_scaling = True
        >>> detach(TimeSignature, measure)
        (TimeSignature((4, 12)),)
        >>> new_time_signature = TimeSignature((5, 12))
        >>> attach(new_time_signature, measure)
        >>> measure.is_underfull
        True

    ::

        >>> scoretools.append_spacer_skip_to_underfull_measure(measure)
        Measure((5, 12), "c'8 d'8 e'8 f'8 s1 * 1/8", implicit_scaling=True)

    ..  doctest::

        >>> print(format(measure))
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
    from abjad.tools import scoretools

    assert isinstance(measure, scoretools.Measure)

    if measure.is_underfull:
        target_duration = measure.time_signature.duration
        duration = measure._get_duration()
        skip = scoretools.Skip((1, 1))
        time_signature_multiplier = \
            measure.time_signature.implied_prolation
        new_duration = target_duration - duration
        new_multiplier = new_duration.__div__(time_signature_multiplier)
        attach(new_multiplier, skip)
        measure.append(skip)

    return measure
