# -*- encoding: utf-8 -*-
from experimental import *


def test_SegmentSpecification__look_up_rhythm_set_expression_from_future_between_voices_01():
    r'''From-future rhythm set expression lookup expression between voices.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    red_segment.set_divisions([(1, 8), (2, 8)], contexts=['Voice 1'])
    red_segment.set_divisions([(1, 8), (3, 8)], contexts=['Voice 2'])
    blue_voice_2_rhythm_set_expression = blue_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    red_segment.set_rhythm(blue_voice_2_rhythm_set_expression, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths)
    blue_segment.set_time_signatures([(2, 8), (2, 8)])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_from_future_between_voices_02():
    r'''From-future rhythm set expression lookup expression between voices 
    with reverse callback.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    red_segment.set_divisions([(1, 8), (2, 8)], contexts=['Voice 1'])
    red_segment.set_divisions([(1, 8), (3, 8)], contexts=['Voice 2'])
    blue_voice_2_rhythm_set_expression = blue_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    blue_voice_2_rhythm_set_expression = blue_voice_2_rhythm_set_expression.reflect()
    red_segment.set_rhythm(blue_voice_2_rhythm_set_expression, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths)
    blue_segment.set_time_signatures([(2, 8), (2, 8)])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_from_future_between_voices_03():
    r'''From-future rhythm set expression lookup expression between voices 
    with reverse callback.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    red_segment.set_divisions([(1, 8), (2, 8)], contexts=['Voice 1'])
    red_segment.set_divisions([(1, 8), (3, 8)], contexts=['Voice 2'])
    blue_voice_2_rhythm_set_expression = blue_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    blue_voice_2_rhythm_set_expression = blue_voice_2_rhythm_set_expression.reflect()
    red_segment.set_rhythm(blue_voice_2_rhythm_set_expression, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths)
    blue_segment.set_time_signatures([(2, 8), (2, 8)])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_from_future_between_voices_04():
    r'''From-future rhythm set expression lookup expression between voices 
    with reverse callbacks.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    red_segment.set_divisions([(1, 8), (2, 8)], contexts=['Voice 1'])
    red_segment.set_divisions([(1, 8), (3, 8)], contexts=['Voice 2'])
    blue_voice_2_rhythm_set_expression = blue_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    blue_voice_2_rhythm_set_expression = blue_voice_2_rhythm_set_expression.reflect()
    blue_voice_2_rhythm_set_expression = blue_voice_2_rhythm_set_expression.reflect()
    red_segment.set_rhythm(blue_voice_2_rhythm_set_expression, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths)
    blue_segment.set_time_signatures([(2, 8), (2, 8)])
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
