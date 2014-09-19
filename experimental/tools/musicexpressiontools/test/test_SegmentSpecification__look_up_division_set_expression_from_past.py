# -*- encoding: utf-8 -*-
from experimental import *


def test_SegmentSpecification__look_up_division_set_expression_from_past_01():
    r'''From-past division set expression lookup expression.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    red_segment.set_divisions([(3, 16), (5, 16)])
    red_segment.set_rhythm(library.joined_sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    red_division_set_expression = red_segment.timespan.start_offset.look_up_division_set_expression('Voice 1')
    blue_segment.set_divisions(red_division_set_expression)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)