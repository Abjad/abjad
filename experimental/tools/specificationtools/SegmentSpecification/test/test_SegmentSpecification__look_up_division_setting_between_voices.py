from abjad import *
from experimental.tools import *


def test_SegmentSpecification__look_up_division_setting_between_voices_01():
    '''Division command request between voices.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16), (5, 16)], contexts=['Voice 2'])
    voice_2_division_command = red_segment.timespan.start_offset.look_up_division_setting('Voice 2')
    red_segment.set_divisions(voice_2_division_command, contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_division_setting_between_voices_02():
    '''Division command request between voices with request-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16), (5, 16)], contexts=['Voice 2'])
    voice_2_division_command = red_segment.timespan.start_offset.look_up_division_setting('Voice 2')
    voice_2_division_command = voice_2_division_command.reverse()
    red_segment.set_divisions(voice_2_division_command, contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_division_setting_between_voices_03():
    '''Division command request between voices with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16), (5, 16)], contexts=['Voice 2'])
    voice_2_division_command = red_segment.timespan.start_offset.look_up_division_setting('Voice 2')
    voice_2_division_command = voice_2_division_command.reverse()
    red_segment.set_divisions(voice_2_division_command, contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_division_setting_between_voices_04():
    '''Division command request between voices with both request- and set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(3, 16), (5, 16)], contexts=['Voice 2'])
    voice_2_division_command = red_segment.timespan.start_offset.look_up_division_setting('Voice 2')
    voice_2_division_command = voice_2_division_command.reverse()
    voice_2_division_command = voice_2_division_command.reverse()
    red_segment.set_divisions(voice_2_division_command, contexts=['Voice 1'])
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
