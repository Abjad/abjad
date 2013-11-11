# -*- encoding: utf-8 -*-
from experimental import *


def test_single_segment_solo__nonoverlapping_division_select_expressions_01():
    r'''Nonoverlapping measure select expressions.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    first_measure = red_segment.select_measures('Voice 1')[:1]
    first_measure.timespan.set_divisions([(2, 32)])
    second_measure = red_segment.select_measures('Voice 1')[1:2]
    second_measure.timespan.set_divisions([(3, 32)])
    third_measure = red_segment.select_measures('Voice 1')[2:3]
    third_measure.timespan.set_divisions([(4, 32)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
