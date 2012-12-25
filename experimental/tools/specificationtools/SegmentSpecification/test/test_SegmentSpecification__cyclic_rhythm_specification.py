from abjad import *
from experimental.tools import *
import py


def test_SegmentSpecification__cyclic_rhythm_specification_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_rhythm = red_segment.select_leaves('Voice 1') 
    blue_rhythm = blue_segment.select_leaves('Voice 1')
    red_segment.set_rhythm(blue_rhythm)

    assert py.test.raises(Exception, 'score_specification.interpret()')
