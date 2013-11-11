# -*- encoding: utf-8 -*-
from experimental import *


def test_multiple_voice_duo_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=[2, 2])
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(4, 16)], contexts=['Voice 1-1', 'Voice 2-1'])
    red_segment.set_divisions([(3, 16)], contexts=['Voice 1-2', 'Voice 2-2'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    #assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
