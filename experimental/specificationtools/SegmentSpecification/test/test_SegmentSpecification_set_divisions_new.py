from abjad.tools import *
from experimental import *
from experimental.specificationtools import library
import py


# TODO: IMPLEMENT ME
def test_SegmentSpecification_get_timespan_from_measures_01():
    '''Measure timespan and fractional segment timespan.
    '''
    py.test.skip('working on this one now')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment('red')
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    first_measure = segment.select_background_measures(stop=1).timespan
    second_measure = segment.select_background_measures(start=-1).timespan
    first_half = segment.select_segment_duration_ratio_item((1, 1), 0).timespan
    second_half = segment.select_segment_duration_ratio_item((1, 1), 1).timespan

    segment.set_divisions_new([(3, 16)], timespan=first_measure, contexts=['Voice 1'], persist=False)
    segment.set_divisions_new([(5, 16)], timespan=second_measure, contexts=['Voice 1'], persist=False)

    segment.set_divisions_new([(5, 16)], timespan=first_measure, contexts=['Voice 2'], persist=False)
    segment.set_divisions_new([(3, 16)], timespan=second_measure, contexts=['Voice 2'], persist=False)

    segment.set_divisions_new([(3, 16)], timespan=first_half, contexts=['Voice 3'], persist=False)
    segment.set_divisions_new([(5, 16)], timespan=second_half, contexts=['Voice 3'], persist=False)

    segment.set_divisions_new([(5, 16)], timespan=first_half, contexts=['Voice 4'], persist=False)
    segment.set_divisions_new([(3, 16)], timespan=second_half, contexts=['Voice 4'], persist=False)

    segment.set_rhythm(segment, library.thirty_seconds)
    segment = score_specification.append_segment()
    score = score_specification.interpret()
