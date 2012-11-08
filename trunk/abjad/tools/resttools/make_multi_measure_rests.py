from abjad.tools import durationtools


def make_multi_measure_rests(durations):
    '''.. versionadded:: 2.0

    Make multi-measure rests from `durations`::

        >>> resttools.make_multi_measure_rests([(4, 4), (7, 4)])
        [MultiMeasureRest('R1'), MultiMeasureRest('R1..')]

    Return list.
    '''
    from abjad.tools import resttools

    multi_measure_rests = []

    for duration in durations:
        written_duration = durationtools.Duration(duration)
        if not written_duration.is_assignable:
            raise AssignabilityError('multi-measure rest durations must be assignable.')
        multi_measure_rest = resttools.MultiMeasureRest(written_duration)
        multi_measure_rests.append(multi_measure_rest)

    return multi_measure_rests
