from abjad.tools import durationtools


def make_multi_measure_rests(duration_tokens):
    '''.. versionadded:: 2.0

    Make multi-measure rests from `duration_tokens`::

        >>> resttools.make_multi_measure_rests([(4, 4), (7, 4)])
        [MultiMeasureRest('R1'), MultiMeasureRest('R1..')]

    Return list.
    '''
    from abjad.tools import resttools

    multi_measure_rests = []

    for duration_token in duration_tokens:
        written_duration = durationtools.duration_token_to_rational(duration_token)
        if not durationtools.is_assignable_rational(written_duration):
            raise AssignabilityError('multi-measure rest durations must be assignable.')
        multi_measure_rest = resttools.MultiMeasureRest(written_duration)
        multi_measure_rests.append(multi_measure_rest)

    return multi_measure_rests
