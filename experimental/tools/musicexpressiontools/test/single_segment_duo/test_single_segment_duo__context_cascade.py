# -*- encoding: utf-8 -*-
from experimental import *


def test_single_segment_duo__context_cascade_01():
    r'''Lower-level context set expression overrides higher-level 
    context set expression.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.joined_sixteenths)
    red_segment.set_rhythm(library.note_tokens, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
