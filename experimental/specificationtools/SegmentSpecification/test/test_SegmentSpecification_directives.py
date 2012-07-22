from abjad.tools import *
from experimental.specificationtools.ScoreSpecification import ScoreSpecification


def test_SegmentSpecification_directives_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = ScoreSpecification(score_template)

    segment = specification.append_segment()
    assert not segment.directives
    assert not segment.settings

    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    assert len(segment.directives) == 1
    assert not segment.settings

    score = specification.interpret()
    assert len(segment.directives) == 1
    assert len(segment.settings) == 1
