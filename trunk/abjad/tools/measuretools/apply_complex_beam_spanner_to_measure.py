from abjad.tools.measuretools.Measure import Measure
from abjad.tools.spannertools import DuratedComplexBeamSpanner


def apply_complex_beam_spanner_to_measure(measure):
    r'''.. versionadded:: 2.0

    Apply complex beam spanner to `measure`::

        abjad> measure = Measure((2, 8), "c'8 d'8")

    ::

        abjad> f(measure)
        {
            \time 2/8
            c'8
            d'8
        }

    ::

        abjad> measuretools.apply_complex_beam_spanner_to_measure(measure)
        DuratedComplexBeamSpanner(|2/8(2)|)

    ::

        abjad> f(measure)
        {
            \time 2/8
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #1
            c'8 [
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #0
            d'8 ]
        }


    Return complex beam spanner.
    '''

    # check measure type
    if not isinstance(measure, Measure):
        raise TypeError('must be measure: %s' % measure)

    # apply complex beam spanner to measure
    beam = DuratedComplexBeamSpanner(measure)

    # return beam spanner
    return beam
