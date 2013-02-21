from experimental import *


def test_TimespanExpression__callbacks_01():
    '''Scale timespan.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:1]
    timespan = measures.timespan.scale(Multiplier(4))
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_TimespanExpression__callbacks_02():
    '''Set timespan duration.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:1]
    timespan = measures.timespan.set_duration(Duration(2, 8))
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_TimespanExpression__callbacks_03():
    '''Set timespan start offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:2]
    timespan = measures.timespan.set_offsets(start_offset=Offset(1, 8))
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_TimespanExpression__callbacks_04():
    '''Set timespan stop offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:1]
    timespan = measures.timespan.set_offsets(stop_offset=Offset(2, 8))
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_TimespanExpression__callbacks_05():
    '''Translate timespan.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:1]
    timespan = measures.timespan.translate_offsets(Duration(1, 8), Duration(1, 8)) 
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_TimespanExpression__callbacks_06():
    '''Translate timespan start offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:2]
    timespan = measures.timespan.translate_offsets(start_offset_translation=Duration(1, 8)) 
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_TimespanExpression__callbacks_07():
    '''Translate timespan stop offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:2]
    timespan = measures.timespan.translate_offsets(stop_offset_translation=Duration(-1, 8)) 
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_TimespanExpression__callbacks_08():
    '''Stacked timespan callbacks applied in composition.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_measures('Voice 1')[:2]
    timespan = measures.timespan.translate_offsets(start_offset_translation=Duration(1, 8))
    timespan = timespan.scale(Multiplier(2))
    timespan.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
