# -*- encoding: utf-8 -*-
from experimental import *


def test_SegmentSpecification__set_divisions_01():
    r'''Set divisions from time signatures.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    time_signatures = red_segment.select_time_signatures('Voice 1')
    time_signatures = time_signatures.reflect()
    red_segment.set_divisions(time_signatures, contexts=['Voice 1'])
    red_segment.set_rhythm(library.joined_sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)