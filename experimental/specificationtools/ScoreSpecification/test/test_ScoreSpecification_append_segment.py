from abjad.tools import *
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
import py


def test_ScoreSpecification_append_segment_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = ScoreSpecification(score_template)

    segment = specification.append_segment()
    assert segment.segment_name == '1'
    assert len(specification.segment_specifications) == 1
    
    segment = specification.append_segment(name='foo')
    assert segment.segment_name == 'foo'
    assert len(specification.segment_specifications) == 2


def test_ScoreSpecification_append_segment_02():
    '''Error on duplicate segment name.
    '''

    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = ScoreSpecification(score_template)

    specification.append_segment('1')

    py.test.raises(Exception, "specification.append_segment('1')")
