from abjad.tools.measuretools.Measure import Measure


def append_spacer_skip_to_underfull_measure(rigid_measure):
    r'''.. versionadded:: 1.1

    Append spacer skip to underfull `measure`::

        abjad> measure = Measure((4, 12), "c'8 d'8 e'8 f'8")
        abjad> contexttools.detach_time_signature_marks_attached_to_component(measure)
        (TimeSignatureMark((4, 12)),)
        abjad> contexttools.TimeSignatureMark((5, 12))(measure)
        TimeSignatureMark((5, 12))(|5/12, c'8, d'8, e'8, f'8|)
        abjad> measure.is_underfull
        True

    ::

        abjad> measuretools.append_spacer_skip_to_underfull_measure(measure)
        Measure(5/12, [c'8, d'8, e'8, f'8, s1 * 1/8])

    ::

        abjad> f(measure)
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

    .. versionchanged:: 2.0
        renamed ``measuretools.make_measures_with_full_measure_spacer_skips_underfull_spacer_skip()`` to
        ``measuretools.append_spacer_skip_to_underfull_measure()``.
    '''
    from abjad.tools import contexttools
    from abjad.tools.skiptools.Skip import Skip

    assert isinstance(rigid_measure, Measure)

    if rigid_measure.is_underfull:
        target_duration = contexttools.get_effective_time_signature(rigid_measure).duration
        prolated_duration = rigid_measure.prolated_duration
        skip = Skip((1, 1))
        meter_multiplier = contexttools.get_effective_time_signature(rigid_measure).multiplier
        new_multiplier = (target_duration - prolated_duration) / meter_multiplier
        skip.duration_multiplier = new_multiplier
        rigid_measure.append(skip)

    return rigid_measure
