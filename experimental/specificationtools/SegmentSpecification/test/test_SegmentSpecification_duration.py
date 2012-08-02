from abjad.tools import *
from experimental import *


def test_SegmentSpecification_duration_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment('red')
    assert segment.duration == durationtools.Duration(0)

    segment.set_time_signatures([(4, 8), (3, 8)])
    assert segment.duration == durationtools.Duration(0)

    score = score_specification.interpret()
    assert segment.duration == durationtools.Duration(7, 8)
