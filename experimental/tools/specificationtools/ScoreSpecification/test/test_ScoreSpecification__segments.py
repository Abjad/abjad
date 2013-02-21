from abjad.tools import *
from experimental import *


def test_ScoreSpecification__segments_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    assert not score_specification.specification.segment_specifications


def test_ScoreSpecification__segments_02():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)

    score_specification.append_segment(name='red')
    assert len(score_specification.specification.segment_specifications) == 1

    score_specification.append_segment(name='blue')
    assert len(score_specification.specification.segment_specifications) == 2

    score_specification.pop()
    assert len(score_specification.specification.segment_specifications) == 1
