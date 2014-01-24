# -*- encoding: utf-8 -*-
from experimental import *


def test_MeasureSelectExpression__select_leaves_01():
    r'''Select measures and then select leaves.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_sixteenths)
    slur = spannertools.Slur()
    measures = red_segment.select_measures('Voice 1')[1:3].select_leaves('Voice 1').set_spanner(slur)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
