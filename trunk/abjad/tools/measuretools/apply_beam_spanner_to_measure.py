from abjad.tools.measuretools.Measure import Measure
from abjad.tools.spannertools import BeamSpanner


def apply_beam_spanner_to_measure(measure):
    r'''.. versionadded:: 2.0

    Apply beam spanner to `measure`::

        abjad> measure = Measure((2, 8), "c'8 d'8")

    ::

        abjad> f(measure)
        {
            \time 2/8
            c'8
            d'8
        }

    ::

        abjad> measuretools.apply_beam_spanner_to_measure(measure)
        BeamSpanner(|2/8(2)|)

    ::

        abjad> f(measure)
        {
            \time 2/8
            c'8 [
            d'8 ]
        }

    Return beam spanner.
    '''

    # check measure type
    if not isinstance(measure, Measure):
        raise TypeError('must be measure: %s' % measure)

    # apply beam spanner to measure
    beam = BeamSpanner(measure)

    # return beam spanner
    return beam
