# -*- encoding: utf-8 -*-
from experimental import *
import pytest


def test_SegmentSpecification__cyclic_division_specification_01():

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_divisions = red_segment.select_divisions('Voice 1')
    blue_divisions = blue_segment.select_divisions('Voice 1')
    red_segment.set_divisions(blue_divisions)
    blue_segment.set_divisions(red_divisions)

    assert pytest.raises(Exception, 'score_specification.interpret()')
