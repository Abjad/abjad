from abjad import *
from experimental import *


def test_SegmentSpecification__look_up_time_signature_setting_from_past_01():
    '''From-past time signature command reqeust.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment = score_specification.append_segment(name='blue')
    red_time_signature_command = red_segment.timespan.start_offset.look_up_time_signature_setting('Voice 1')
    blue_segment.set_time_signatures(red_time_signature_command)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_time_signature_setting_from_past_02():
    '''From-past time signature command reqeust with request-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment = score_specification.append_segment(name='blue')
    red_time_signature_command = red_segment.timespan.start_offset.look_up_time_signature_setting('Voice 1')
    red_time_signature_command = red_time_signature_command.reflect()
    blue_segment.set_time_signatures(red_time_signature_command)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_time_signature_setting_from_past_03():
    '''From-past time signature command reqeust with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment = score_specification.append_segment(name='blue')
    red_time_signature_command = red_segment.timespan.start_offset.look_up_time_signature_setting('Voice 1')
    red_time_signature_command = red_time_signature_command.reflect()
    blue_segment.set_time_signatures(red_time_signature_command)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_time_signature_setting_from_past_04():
    '''From-past time signature command request with both request- and set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment = score_specification.append_segment(name='blue')
    red_time_signature_command = red_segment.timespan.start_offset.look_up_time_signature_setting('Voice 1')
    red_time_signature_command = red_time_signature_command.reflect()
    red_time_signature_command = red_time_signature_command.reflect()
    blue_segment.set_time_signatures(red_time_signature_command)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
