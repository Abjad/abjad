from abjad.tools import *
from experimental.specificationtools.ScoreSpecification import ScoreSpecification


def test_SegmentSpecification_multiple_context_settings_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = ScoreSpecification(score_template)

    segment = specification.append_segment()
    assert not segment.multiple_context_settings
    assert not segment.single_context_settings

    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    assert len(segment.multiple_context_settings) == 1
    assert not segment.single_context_settings

    score = specification.interpret()
    assert len(segment.multiple_context_settings) == 1
    assert len(segment.single_context_settings) == 1
