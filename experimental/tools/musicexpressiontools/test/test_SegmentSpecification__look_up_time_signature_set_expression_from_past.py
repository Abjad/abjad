# -*- encoding: utf-8 -*-
from experimental import *


def test_SegmentSpecification__look_up_time_signature_set_expression_from_past_01():
    r'''From-past time signature set expression lookup expression.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment = score_specification.append_segment(name='blue')
    red_time_signature_set_expression = \
        red_segment.timespan.start_offset.look_up_time_signature_set_expression('Voice 1')
    blue_segment.set_time_signatures(red_time_signature_set_expression)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_time_signature_set_expression_from_past_02():
    r'''From-past time signature set expression lookup expression
    with reverse callback.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment = score_specification.append_segment(name='blue')
    red_time_signature_set_expression = \
        red_segment.timespan.start_offset.look_up_time_signature_set_expression('Voice 1')
    red_time_signature_set_expression = red_time_signature_set_expression.reflect()
    blue_segment.set_time_signatures(red_time_signature_set_expression)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_time_signature_set_expression_from_past_03():
    r'''From-past time signature set expression lookup expression
    with reverse callback.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment = score_specification.append_segment(name='blue')
    red_time_signature_set_expression = \
        red_segment.timespan.start_offset.look_up_time_signature_set_expression('Voice 1')
    red_time_signature_set_expression = red_time_signature_set_expression.reflect()
    blue_segment.set_time_signatures(red_time_signature_set_expression)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_time_signature_set_expression_from_past_04():
    r'''From-past time signature set expression lookup expression
    with reverse callbacks.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment = score_specification.append_segment(name='blue')
    red_time_signature_set_expression = \
        red_segment.timespan.start_offset.look_up_time_signature_set_expression('Voice 1')
    red_time_signature_set_expression = red_time_signature_set_expression.reflect()
    red_time_signature_set_expression = red_time_signature_set_expression.reflect()
    blue_segment.set_time_signatures(red_time_signature_set_expression)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)