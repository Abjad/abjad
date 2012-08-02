from abjad.tools import *
from experimental import *
import py


def test_ScoreSpecification_append_segment_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = specificationtools.ScoreSpecification(score_template)

    segment = specification.append_segment('red')
    assert segment.segment_name == 'red'
    assert len(specification.segment_specifications) == 1
    
    segment = specification.append_segment('blue')
    assert segment.segment_name == 'blue'
    assert len(specification.segment_specifications) == 2


def test_ScoreSpecification_append_segment_02():
    '''Error on duplicate segment name.
    '''

    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = specificationtools.ScoreSpecification(score_template)

    specification.append_segment('red')

    py.test.raises(Exception, "specification.append_segment('red')")
