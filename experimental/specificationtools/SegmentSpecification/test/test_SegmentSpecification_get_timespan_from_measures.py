from abjad.tools import *
from experimental import helpertools
from experimental import specificationtools
from experimental.specificationtools import library
import py


# TODO: modernize this test file and then rename it
def test_SegmentSpecification_get_timespan_from_measures_01():
    '''Measure timespan and fractional segment timespan.
    '''
    py.test.skip('working on this one now')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment('red')
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

    segment = score_specification.append_segment()

    score = score_specification.interpret()
