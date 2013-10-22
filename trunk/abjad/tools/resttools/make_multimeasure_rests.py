# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import selectiontools


def make_multimeasure_rests(durations):
    '''Make multi-measure rests from `durations`:

    ::

        >>> resttools.make_multimeasure_rests([(4, 4), (7, 4)])
        Selection(MultimeasureRest('R1'), MultimeasureRest('R1..'))

    Returns list.
    '''
    from abjad.tools import resttools

    multimeasure_rests = []

    for duration in durations:
        written_duration = durationtools.Duration(duration)
        if not written_duration.is_assignable:
            raise AssignabilityError('multi-measure rest durations must be assignable.')
        multimeasure_rest = resttools.MultimeasureRest(written_duration)
        multimeasure_rests.append(multimeasure_rest)

    result = selectiontools.Selection(multimeasure_rests)
    return result
