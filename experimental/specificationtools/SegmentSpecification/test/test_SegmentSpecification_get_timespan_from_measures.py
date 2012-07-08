from abjad.tools import *
from experimental.specificationtools import helpers
from experimental.specificationtools import library
from experimental.specificationtools import ScoreSpecification
import py


def test_SegmentSpecification_get_timespan_from_measures_01():
    '''Measure timespan and fractional segment timespan.
    '''
    py.test.skip('working on this one now')

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=4))

    segment = specification.append_segment('red')
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    first = segment.get_timespan_from_measures(0)
    second = segment.get_timespan_from_measures(-1)
    segment.set_divisions('Voice 1', [(3, 16)], timespan=first, persist=False)
    segment.set_divisions('Voice 1', [(5, 16)], timespan=second, persist=False)

    segment.set_divisions('Voice 2', [(5, 16)], timespan=first, persist=False)
    segment.set_divisions('Voice 2', [(3, 16)], timespan=second, persist=False)

    first = segment.get_timespan(stop=Fraction(1, 2))
    second = segment.get_timespan(start=Fraction(1, 2))
    segment.set_divisions('Voice 3', [(3, 16)], timespan=first, persist=False)
    segment.set_divisions('Voice 3', [(5, 16)], timespan=second, persist=False)

    segment.set_divisions('Voice 4', [(5, 16)], timespan=first, persist=False)
    segment.set_divisions('Voice 4', [(3, 16)], timespan=second, persist=False)

    segment.set_rhythm(segment, library.thirty_seconds)

    segment = specification.append_segment()

    score = specification.interpret()
