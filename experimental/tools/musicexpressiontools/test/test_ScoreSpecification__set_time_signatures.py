# -*- encoding: utf-8 -*-
from experimental import *


def test_ScoreSpecification__set_time_signatures_01():
    r'''Works without segment specification.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    score_specification.set_divisions([(3, 16)])
    score_specification.set_rhythm(library.joined_sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_time_signatures_02():
    r'''Works without division specification.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    score_specification.set_rhythm(library.joined_sixteenths)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
