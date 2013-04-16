from experimental import *


def test_SegmentSpecification__look_up_time_signature_set_expression_from_future_01():
    '''From-future time signature set expression lookup expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    blue_time_signature_set_expression = blue_segment.timespan.start_offset.look_up_time_signature_set_expression('Voice 1')
    red_segment.set_time_signatures(blue_time_signature_set_expression)
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_time_signature_set_expression_from_future_02():
    '''From-future time signature set expression lookup expression with reverse callback.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    blue_time_signature_set_expression = blue_segment.timespan.start_offset.look_up_time_signature_set_expression('Voice 1')
    blue_time_signature_set_expression = blue_time_signature_set_expression.reflect()
    red_segment.set_time_signatures(blue_time_signature_set_expression)
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_time_signature_set_expression_from_future_03():
    '''From-future time signature set expression lookup expression with reverse callback.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    blue_time_signature_set_expression = blue_segment.timespan.start_offset.look_up_time_signature_set_expression('Voice 1')
    blue_time_signature_set_expression = blue_time_signature_set_expression.reflect()
    red_segment.set_time_signatures(blue_time_signature_set_expression)
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_time_signature_set_expression_from_future_04():
    '''From-future time signature set expression lookup expression with reverse callbacks.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    blue_time_signature_set_expression = blue_segment.timespan.start_offset.look_up_time_signature_set_expression('Voice 1')
    blue_time_signature_set_expression = blue_time_signature_set_expression.reflect()
    blue_time_signature_set_expression = blue_time_signature_set_expression.reflect()
    red_segment.set_time_signatures(blue_time_signature_set_expression)
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
