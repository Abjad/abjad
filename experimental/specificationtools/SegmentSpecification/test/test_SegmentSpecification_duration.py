from abjad.tools import *
from experimental.specificationtools.ScoreSpecification import ScoreSpecification


def test_SegmentSpecification_duration_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = ScoreSpecification(score_template)

    segment = specification.append_segment()
    assert segment.duration is None

    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    assert segment.duration is None

    score = specification.interpret()
    assert segment.duration == durationtools.Duration(7, 8)
