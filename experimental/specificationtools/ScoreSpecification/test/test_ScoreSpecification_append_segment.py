from abjad.tools import *
from experimental import *
import py


def test_ScoreSpecification_make_segment_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.make_segment('red')
    assert segment.segment_name == 'red'
    assert len(score_specification.segment_specifications) == 1
    
    segment = score_specification.make_segment('blue')
    assert segment.segment_name == 'blue'
    assert len(score_specification.segment_specifications) == 2


def test_ScoreSpecification_make_segment_02():
    '''Error on duplicate segment name.
    '''

    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    score_specification.make_segment('red')

    py.test.raises(Exception, "score_specification.make_segment('red')")
