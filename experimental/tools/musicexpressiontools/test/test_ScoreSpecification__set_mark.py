# -*- encoding: utf-8 -*-
from experimental import *


def test_ScoreSpecification__set_mark_01():

    score_template = templatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(2, 16)])
    score_specification.set_rhythm(library.joined_note_tokens)
    score_specification.select_leaves('Voice 1').set_mark(indicatortools.StemTremolo(32))
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
