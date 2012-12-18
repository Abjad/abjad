from abjad import *
from experimental.tools import *


def test_SegmentSpecification__request_division_command_from_past_01():
    '''From-past division command request.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    red_segment.set_divisions([(3, 16), (5, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    red_division_command = red_segment.request_division_command('Voice 1')
    blue_segment.set_divisions(red_division_command)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_division_command_from_past_02():
    '''From-past division command request with request-time reverse.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    red_segment.set_divisions([(3, 16), (5, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    red_division_command = red_segment.request_division_command('Voice 1')
    red_division_command = red_division_command.reverse()
    blue_segment.set_divisions(red_division_command)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_division_command_from_past_03():
    '''From-past division command request with set-time reverse.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    red_segment.set_divisions([(3, 16), (5, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    red_division_command = red_segment.request_division_command('Voice 1')
    red_division_command = red_division_command.reverse()
    blue_segment.set_divisions(red_division_command)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_division_command_from_past_04():
    '''From-past division command request with request- and set-time reverse.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    red_segment.set_divisions([(3, 16), (5, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    red_division_command = red_segment.request_division_command('Voice 1')
    red_division_command = red_division_command.reverse()
    red_division_command = red_division_command.reverse()
    blue_segment.set_divisions(red_division_command)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
