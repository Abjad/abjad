from abjad import *
from experimental import *
import py


def test_SegmentSpecification_request_divisions_01():
    '''Request divisions from earlier segment. Reverse divisions at set-time.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    
    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(4, 16), (3, 16), (2, 16)])
    segment.set_rhythm(library.sixteenths)
    
    segment = score_specification.make_segment(name='blue')
    source = score_specification.request_divisions('Voice 1', 'red', segment_count=1)
    segment.set_divisions(source, reverse=True)

    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_divisions_02():
    '''Request divisions from later segment. Reverse divisions at set-time.
    '''
    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    
    red_segment = score_specification.make_segment(name='red')
    red_segment.set_time_signatures([((2, 8), (2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.sixteenths)
    
    blue_segment = score_specification.make_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (4, 8)]
    blue_segment.set_divisions([(5, 16)])

    green_segment = score_specification.make_segment(name='green', index=1)
    green_segment.set_time_signatures([(3, 8), (3, 8)])
    blue_divisions = blue_segment.request_divisions('Voice 1')
    green_segment.set_divisions(blue_divisions, reverse=True)

    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
