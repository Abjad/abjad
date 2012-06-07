from abjad.tools import *
from specificationtools.ScoreSpecification import ScoreSpecification
import py


def test_ScoreSpecification_append_segment_01():

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))

    segment = specification.append_segment()
    assert segment.name == '1'
    assert len(specification.segments) == 1
    
    segment = specification.append_segment(name='foo')
    assert segment.name == 'foo'
    assert len(specification.segments) == 2


def test_ScoreSpecification_append_segment_02():
    '''Error on duplicate segment name.
    '''

    
    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    specification.append_segment('1')

    py.test.raises(Exception, "specification.append_segment('1')")
