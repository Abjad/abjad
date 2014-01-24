# -*- encoding: utf-8 -*-
from experimental import *


def test_CounttimeComponentSelectExpression__evaluate_against_score_01():
    r'''Score-evaluate counttime component select expression anchored to 
    division select expression.
    '''

    score_template = templatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(6 * [(2, 8)])
    score_specification.set_divisions([(3, 16)])
    score_specification.set_rhythm(library.sixteenths)
    left, right = score_specification.select_divisions('Voice 1').partition_by_ratio((1, 1))
    left, right = left.timespan.select_leaves('Voice 1'), right.timespan.select_leaves('Voice 1')
    left.set_pitch(library.example_pitches_1(reverse=True))
    right.set_pitch(library.example_pitches_1(reverse=True))
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
