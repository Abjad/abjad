from experimental import *
import pytest


pytest.skip('FIXME')
def test_SegmentSpecification__look_up_division_set_expression_from_past_between_voices_01():
    '''From-past division set expression lookup expression between voices.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (2, 8)])
    red_segment.set_divisions([(2, 16), (3, 16)], contexts=['Voice 1'])
    red_segment.set_divisions([(2, 16), (5, 16)], contexts=['Voice 2'])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    red_voice_2_division_set_expression = red_segment.timespan.start_offset.look_up_division_set_expression('Voice 2')
    blue_segment.set_divisions(red_voice_2_division_set_expression, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_division_set_expression_from_past_between_voices_02():
    '''From-past division set expression lookup expression between voices with reverse callback.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (2, 8)])
    red_segment.set_divisions([(2, 16), (3, 16)], contexts=['Voice 1'])
    red_segment.set_divisions([(2, 16), (5, 16)], contexts=['Voice 2'])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    red_voice_2_division_set_expression = red_segment.timespan.start_offset.look_up_division_set_expression('Voice 2')
    red_voice_2_division_set_expression = red_voice_2_division_set_expression.reflect()
    blue_segment.set_divisions(red_voice_2_division_set_expression, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_division_set_expression_from_past_between_voices_03():
    '''From-past division set expression lookup expression between voices with reverse callback.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (2, 8)])
    red_segment.set_divisions([(2, 16), (3, 16)], contexts=['Voice 1'])
    red_segment.set_divisions([(2, 16), (5, 16)], contexts=['Voice 2'])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    red_voice_2_division_set_expression = red_segment.timespan.start_offset.look_up_division_set_expression('Voice 2')
    red_voice_2_division_set_expression = red_voice_2_division_set_expression.reflect()
    blue_segment.set_divisions(red_voice_2_division_set_expression, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_division_set_expression_from_past_between_voices_04():
    '''From-past division set expression lookup expression between voices with reverse callbacks.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (2, 8)])
    red_segment.set_divisions([(2, 16), (3, 16)], contexts=['Voice 1'])
    red_segment.set_divisions([(2, 16), (5, 16)], contexts=['Voice 2'])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    red_voice_2_division_set_expression = red_segment.timespan.start_offset.look_up_division_set_expression('Voice 2')
    red_voice_2_division_set_expression = red_voice_2_division_set_expression.reflect()
    red_voice_2_division_set_expression = red_voice_2_division_set_expression.reflect()
    blue_segment.set_divisions(red_voice_2_division_set_expression, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
