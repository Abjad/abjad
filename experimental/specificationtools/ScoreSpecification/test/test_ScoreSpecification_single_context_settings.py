from abjad.tools import *
from experimental import specificationtools


def test_ScoreSpecification_single_context_settings_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    assert not score_specification.single_context_settings

    segment = score_specification.make_segment('red')
    assert not score_specification.single_context_settings
    assert not segment.single_context_settings

    segment.set_time_signatures([(4, 8), (3, 8)])
    assert not score_specification.single_context_settings
    assert not segment.single_context_settings

    score = score_specification.interpret()
    assert len(score_specification.single_context_settings) == 1
    assert len(segment.single_context_settings) == 1
