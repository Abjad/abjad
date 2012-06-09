from abjad.tools import *
from experimental.specificationtools.ScoreSpecification import ScoreSpecification


def test_SegmentSpecification_time_signatures_01():

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))

    segment = specification.append_segment()
    assert segment.time_signatures is None

    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    assert segment.time_signatures is None

    score = specification.interpret()
    assert segment.time_signatures == [(4, 8), (3, 8)]
