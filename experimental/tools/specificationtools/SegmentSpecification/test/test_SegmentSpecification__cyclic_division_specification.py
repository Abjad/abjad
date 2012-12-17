from abjad import *
from experimental import *
import py


def test_SegmentSpecification__cyclic_division_specification_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_divisions = red_segment.request_divisions('Voice 1')
    blue_divisions = blue_segment.request_divisions('Voice 1')
    red_segment.set_divisions(blue_divisions)
    blue_segment.set_divisions(red_divisions)

    assert py.test.raises(exceptions.CyclicSpecificationError, 'score_specification.interpret()')
