from experimental import *


def test_SegmentSpecification__look_up_rhythm_set_expression_from_past_between_voices_01():
    '''From-past set-rhythm lookup expression between voices.
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
    red_voice_2_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    blue_segment.set_rhythm(red_voice_2_rhythm_set_expression, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_from_past_between_voices_02():
    '''From-past set-rhythm lookup expression between voices with reverse callback.
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
    red_voice_2_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    red_voice_2_rhythm_set_expression = red_voice_2_rhythm_set_expression.reflect()
    blue_segment.set_rhythm(red_voice_2_rhythm_set_expression, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_from_past_between_voices_03():
    '''From-past set-rhythm lookup expression between voices with set-time reverse.
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
    red_voice_2_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    red_voice_2_rhythm_set_expression = red_voice_2_rhythm_set_expression.reflect()
    blue_segment.set_rhythm(red_voice_2_rhythm_set_expression, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_from_past_between_voices_04():
    '''From-past set-rhythm lookup expression between voices with reverse callbacks.
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
    red_voice_2_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    red_voice_2_rhythm_set_expression = red_voice_2_rhythm_set_expression.reflect()
    red_voice_2_rhythm_set_expression = red_voice_2_rhythm_set_expression.reflect()
    blue_segment.set_rhythm(red_voice_2_rhythm_set_expression, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
