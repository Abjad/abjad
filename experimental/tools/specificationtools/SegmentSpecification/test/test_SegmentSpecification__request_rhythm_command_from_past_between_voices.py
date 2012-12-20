from abjad import *
from experimental.tools import *


def test_SegmentSpecification__request_rhythm_command_from_past_between_voices_01():
    '''From-past rhythm command request between voices.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (2, 8)])
    red_segment.set_divisions([(1, 8), (2, 8)], contexts=['Voice 1'])
    red_segment.set_divisions([(2, 8), (3, 8)], contexts=['Voice 2'])
    red_segment.set_rhythm(library.dotted_sixteenths)
    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    red_voice_2_rhythm_command = red_segment.start_offset.request_rhythm_command('Voice 2')
    blue_segment.set_rhythm(red_voice_2_rhythm_command, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_rhythm_command_from_past_between_voices_02():
    '''From-past rhythm command request between voices with request-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (2, 8)])
    red_segment.set_divisions([(1, 8), (2, 8)], contexts=['Voice 1'])
    red_segment.set_divisions([(2, 8), (3, 8)], contexts=['Voice 2'])
    red_segment.set_rhythm(library.dotted_sixteenths)
    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    red_voice_2_rhythm_command = red_segment.start_offset.request_rhythm_command('Voice 2')
    red_voice_2_rhythm_command = red_voice_2_rhythm_command.reverse()
    blue_segment.set_rhythm(red_voice_2_rhythm_command, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_rhythm_command_from_past_between_voices_03():
    '''From-past rhythm command request between voices with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (2, 8)])
    red_segment.set_divisions([(1, 8), (2, 8)], contexts=['Voice 1'])
    red_segment.set_divisions([(2, 8), (3, 8)], contexts=['Voice 2'])
    red_segment.set_rhythm(library.dotted_sixteenths)
    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    red_voice_2_rhythm_command = red_segment.start_offset.request_rhythm_command('Voice 2')
    red_voice_2_rhythm_command = red_voice_2_rhythm_command.reverse()
    blue_segment.set_rhythm(red_voice_2_rhythm_command, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_rhythm_command_from_past_between_voices_04():
    '''From-past rhythm command request between voices with both request- and set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (2, 8)])
    red_segment.set_divisions([(1, 8), (2, 8)], contexts=['Voice 1'])
    red_segment.set_divisions([(2, 8), (3, 8)], contexts=['Voice 2'])
    red_segment.set_rhythm(library.dotted_sixteenths)
    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    red_voice_2_rhythm_command = red_segment.start_offset.request_rhythm_command('Voice 2')
    red_voice_2_rhythm_command = red_voice_2_rhythm_command.reverse()
    red_voice_2_rhythm_command = red_voice_2_rhythm_command.reverse()
    blue_segment.set_rhythm(red_voice_2_rhythm_command, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
