from abjad.tools import *
from experimental.tools import specificationtools


def test_ScoreSpecification_single_context_set_expressions_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    assert not score_specification.score_specification.single_context_set_expressions

    red_segment = score_specification.append_segment(name='red')
    assert not score_specification.score_specification.single_context_set_expressions
    assert not score_specification['red'].single_context_set_expressions

    red_segment.set_time_signatures([(4, 8), (3, 8)])
    assert not score_specification.score_specification.single_context_set_expressions
    assert not score_specification['red'].single_context_set_expressions

    score = score_specification.interpret()
    assert len(score_specification.score_specification.single_context_set_expressions) == 1
    assert len(score_specification['red'].single_context_set_expressions) == 1
