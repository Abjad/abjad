from abjad.tools import *
from experimental.tools import *


def test_ScoreSpecification_segments_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    assert not score_specification.segment_specifications


def test_ScoreSpecification_segments_02():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    score_specification.append_segment(name='red')
    assert len(score_specification.segment_specifications) == 1

    score_specification.append_segment(name='blue')
    assert len(score_specification.segment_specifications) == 2

    score_specification.segment_specifications.pop()
    assert len(score_specification.segment_specifications) == 1
