# -*- encoding: utf-8 -*-
from experimental import *


def test_ScoreSpecification__set_rhythm_01():

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    green_segment = score_specification.append_segment(name='green')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    score_specification.set_rhythm(library.joined_eighths)
    blue_segment.set_rhythm(library.joined_sixteenths, persist=False)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
