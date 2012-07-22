from abjad.tools import *
from experimental.specificationtools.ScoreSpecification import ScoreSpecification


def test_SegmentSpecification_time_signatures_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = ScoreSpecification(score_template)

    segment = specification.append_segment()
    assert segment.time_signatures is None

    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    assert segment.time_signatures is None

    score = specification.interpret()
    assert segment.time_signatures == [(4, 8), (3, 8)]
