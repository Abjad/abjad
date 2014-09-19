# -*- encoding: utf-8 -*-
from experimental import *


def test_SegmentSpecification__select_time_signatures_from_future_01():
    r'''From-future time signature select expression.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    blue_time_signatures = blue_segment.select_time_signatures('Voice 1')
    red_segment.set_time_signatures(blue_time_signatures)
    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    blue_segment.set_divisions([(2, 16), (4, 16)])
    blue_segment.set_rhythm(library.joined_sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)