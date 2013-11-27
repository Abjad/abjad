# -*- encoding: utf-8 -*-
from experimental import *


def test_SegmentSpecification__set_time_signatures_corner_cases_01():
    r'''Multiple time signature set expressions are allowed for a single segment.

    Interpreter ignores all but the last.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 8)])
    red_segment.set_time_signatures([(4, 8), (4, 8)])
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
