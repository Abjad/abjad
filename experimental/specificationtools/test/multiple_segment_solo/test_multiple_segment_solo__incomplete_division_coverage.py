from abjad import *
from experimental import *
import py


def test_multiple_segment_solo__incomplete_division_coverage_01():
    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_background_measures('Voice 1', 0, 1)
    right_measure = red_segment.select_background_measures('Voice 1', 1, 2)
    red_segment.set_divisions([(4, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')


def test_multiple_segment_solo__incomplete_division_coverage_02():
    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_background_measures('Voice 1', 0, 1)
    right_measure = red_segment.select_background_measures('Voice 1', 1, 2)
    red_segment.set_divisions([(4, 16)], contexts=['Voice 1'], selector=left_measure)
    red_segment.set_divisions([(5, 16)], contexts=['Voice 1'], selector=right_measure, persist=False)
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
