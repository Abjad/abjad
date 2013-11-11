# -*- encoding: utf-8 -*-
from experimental import *
import pytest


def test_multiple_segment_solo__incomplete_division_coverage_01():
    r'''Divisions specified for one measure and one measure only.
    Other regions default to full-measure divisions.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_measures('Voice 1')[:1]
    left_measure.timespan.set_divisions([(4, 16)], persist=False)
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo__incomplete_division_coverage_02():
    r'''Divisions specified for persistent measure.
    Other regions default to full-measure divisions.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_measures('Voice 1')[:1]
    left_measure.timespan.set_divisions([(4, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo__incomplete_division_coverage_03():
    r'''Divisions specified for two measures separately.
    One measure persists while the other does not.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(6, 8), (3, 8)])
    left_measure = red_segment.select_measures('Voice 1')[:1]
    right_measure = red_segment.select_measures('Voice 1')[1:2]
    left_measure.timespan.set_divisions([(4, 16)], contexts=['Voice 1'])
    right_measure.timespan.set_divisions([(2, 16)], contexts=['Voice 1'], persist=False)
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
