from abjad import *
from experimental import *


def test_SegmentSpecification_request_divisions_01():
    '''From-past division material request with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    
    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    red_segment.set_divisions([(4, 16), (3, 16), (2, 16)])
    red_segment.set_rhythm(library.sixteenths)
    
    blue_segment = score_specification.make_segment(name='blue')
    red_divisions = score_specification.request_divisions('Voice 1', 'red', segment_count=1)
    blue_segment.set_divisions(red_divisions, reverse=True)

    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_divisions_02():
    '''From-future division material request.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    
    red_segment = score_specification.make_segment(name='red')
    blue_segment = score_specification.make_segment(name='blue')

    red_segment.set_time_signatures([(2, 8), (2, 8)])
    blue_divisions = blue_segment.request_divisions('Voice 1')
    red_segment.set_divisions(blue_divisions)
    red_segment.set_rhythm(library.sixteenths)
    
    blue_segment.set_time_signatures([(4, 8), (4, 8)])
    blue_segment.set_divisions([(5, 16)])

    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
