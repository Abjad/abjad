# -*- encoding: utf-8 -*-
from experimental import *


def test_single_segment_solo__nonbinary_01():
    r'''Nonbinary division.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 5)], contexts=['Voice 1'])
    red_segment.set_rhythm(library.tuplet_monads)
    score = score_specification.interpret()

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
