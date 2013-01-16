from abjad import *
from experimental import *


def test_SegmentSpecification__look_up_rhythm_setting_from_past_01():
    '''From-past rhythm command request.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(6, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    red_rhythm_command = red_segment.timespan.start_offset.look_up_rhythm_setting('Voice 1')
    blue_segment.set_rhythm(red_rhythm_command)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_setting_from_past_02():
    '''From-past rhythm command request with request-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.dotted_sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    red_rhythm_command = red_segment.timespan.start_offset.look_up_rhythm_setting('Voice 1')
    red_rhythm_command = red_rhythm_command.reflect()
    blue_segment.set_rhythm(red_rhythm_command)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_setting_from_past_03():
    '''From-past rhythm command request with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.dotted_sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    red_rhythm_command = red_segment.timespan.start_offset.look_up_rhythm_setting('Voice 1')
    red_rhythm_command = red_rhythm_command.reflect()
    blue_segment.set_rhythm(red_rhythm_command)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_setting_from_past_04():
    '''From-past rhythm command request with both request- and set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.dotted_sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    red_rhythm_command = red_segment.timespan.start_offset.look_up_rhythm_setting('Voice 1')
    red_rhythm_command = red_rhythm_command.reflect()
    red_rhythm_command = red_rhythm_command.reflect()
    blue_segment.set_rhythm(red_rhythm_command)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
