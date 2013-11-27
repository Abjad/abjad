# -*- encoding: utf-8 -*-
from experimental import *


def test_multiple_segment_solo__reset_division_select_expressions_01():
    r'''Reset persistent select expressions.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(3, 16)])
    red_segment.set_divisions([(1, 16)], truncate=True)
    middle_two_measures = red_segment.timespan.divide_by_ratio((1, 2, 1))[1]
    middle_two_measures.set_divisions([(2, 16)], persist=True)
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(4 * [(2, 8)])
    blue_segment.set_divisions([(3, 16)])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo__reset_division_select_expressions_02():
    r'''Reset nonpersistent select expressions.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(3, 16)])
    red_segment.set_divisions([(1, 16)], truncate=False)
    middle_two_measures = red_segment.timespan.divide_by_ratio((1, 2, 1))[1]
    middle_two_measures.set_divisions([(2, 16)], persist=True)
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(4 * [(2, 8)])
    blue_segment.set_divisions([(3, 16)])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
