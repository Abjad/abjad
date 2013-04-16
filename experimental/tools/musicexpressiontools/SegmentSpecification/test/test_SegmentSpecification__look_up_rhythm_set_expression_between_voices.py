from experimental import *


def test_SegmentSpecification__look_up_rhythm_set_expression_between_voices_01():
    '''Set-rhythm lookup expression between voices.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    red_segment.set_rhythm(voice_2_rhythm_set_expression, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_between_voices_02():
    '''Set-rhythm lookup expression between voices with reverse callback.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    voice_2_rhythm_set_expression = voice_2_rhythm_set_expression.reflect()
    red_segment.set_rhythm(voice_2_rhythm_set_expression, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_between_voices_03():
    '''Set-rhythm lookup expression between voices with reverse callback.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    voice_2_rhythm_set_expression = voice_2_rhythm_set_expression.reflect()
    red_segment.set_rhythm(voice_2_rhythm_set_expression, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_between_voices_04():
    '''Set-rhythm lookup expression between voices with reverse callbacks.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    voice_2_rhythm_set_expression = voice_2_rhythm_set_expression.reflect()
    voice_2_rhythm_set_expression = voice_2_rhythm_set_expression.reflect()
    red_segment.set_rhythm(voice_2_rhythm_set_expression, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_between_voices_05():
    '''Set-rhythm lookup expression between voices. From parseable string.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    red_segment.set_rhythm(voice_2_rhythm_set_expression, contexts=['Voice 1'])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }", contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_between_voices_06():
    '''Set-rhythm lookup expression between voices with reflect callback.
    From parseable string.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    voice_2_rhythm_set_expression = voice_2_rhythm_set_expression.reflect()
    red_segment.set_rhythm(voice_2_rhythm_set_expression, contexts=['Voice 1'])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }", contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_between_voices_07():
    '''Set-rhythm lookup expression between voices with canceling successive reflect callbacks.
    From parseable string.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 2')
    voice_2_rhythm_set_expression = voice_2_rhythm_set_expression.reflect()
    voice_2_rhythm_set_expression = voice_2_rhythm_set_expression.reflect()
    red_segment.set_rhythm(voice_2_rhythm_set_expression, contexts=['Voice 1'])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }", contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
