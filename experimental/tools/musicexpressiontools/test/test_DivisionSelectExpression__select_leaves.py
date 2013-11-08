# -*- encoding: utf-8 -*-
from experimental import *


def test_DivisionSelectExpression__select_leaves_01():
    r'''Select divisions and then select leaves.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)
    slur = spannertools.Slur()
    red_segment.select_divisions('Voice 1')[1:3].select_leaves('Voice 1').set_spanner(slur)
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)
