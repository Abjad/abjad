from abjad.tools import *
from experimental.tools import *
import py


def test_ScoreSpecification_append_segment_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    assert red_segment.segment_name == 'red'
    assert len(score_specification.segment_specifications) == 1
    
    blue_segment = score_specification.append_segment(name='blue')
    assert blue_segment.segment_name == 'blue'
    assert len(score_specification.segment_specifications) == 2


def test_ScoreSpecification_append_segment_02():
    '''Error on duplicate segment name.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    score_specification.append_segment(name='red')

    py.test.raises(Exception, "score_specification.append_segment(name='red')")
