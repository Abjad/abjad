from experimental import *


def test_SegmentSpecification__look_up_rhythm_set_expression_from_past_01():
    '''From-past rhythm set expression lookup expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(6, 16)])
    red_segment.set_rhythm(library.sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    red_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 1')
    blue_segment.set_rhythm(red_rhythm_set_expression)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_from_past_02():
    '''From-past rhythm set expression lookup expression with reverse callback.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.dotted_sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    red_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 1')
    red_rhythm_set_expression = red_rhythm_set_expression.reflect()
    blue_segment.set_rhythm(red_rhythm_set_expression)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_from_past_03():
    '''From-past rhythm set expression lookup expression with reverse callback.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.dotted_sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    red_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 1')
    red_rhythm_set_expression = red_rhythm_set_expression.reflect()
    blue_segment.set_rhythm(red_rhythm_set_expression)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_from_past_04():
    '''From-past rhythm set expression lookup expression with reverse callbacks.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.dotted_sixteenths)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(4, 8), (5, 8)])
    red_rhythm_set_expression = red_segment.timespan.start_offset.look_up_rhythm_set_expression('Voice 1')
    red_rhythm_set_expression = red_rhythm_set_expression.reflect()
    red_rhythm_set_expression = red_rhythm_set_expression.reflect()
    blue_segment.set_rhythm(red_rhythm_set_expression)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_from_past_05():
    '''Rhythm set expression lookup expression dependent leaf select expression start offset.
    Source is rhythm-maker.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8), (5, 8)])
    measures = red_segment.select_measures('Voice 1')[1:3]
    red_segment.set_rhythm(library.eighths)
    measures.timespan.set_rhythm(library.sixteenths)
    blue_segment.set_rhythm(library.thirty_seconds)
    measures = blue_segment.select_measures('Voice 1')[1:3]
    leaves = red_segment.select_leaves('Voice 1')[:4]
    rhythm_set_expression = leaves.timespan.start_offset.look_up_rhythm_set_expression('Voice 1')
    measures.timespan.set_rhythm(rhythm_set_expression)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_from_past_06():
    '''Rhythm set expression lookup expression dependent leaf select expression stop offset.
    Source is rhythm-maker.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8), (5, 8)])
    measures = red_segment.select_measures('Voice 1')[1:3]
    red_segment.set_rhythm(library.eighths)
    measures.timespan.set_rhythm(library.sixteenths)
    blue_segment.set_rhythm(library.thirty_seconds)
    measures = blue_segment.select_measures('Voice 1')[1:3]
    leaves = red_segment.select_leaves('Voice 1')[:4]
    rhythm_set_expression = leaves.timespan.stop_offset.look_up_rhythm_set_expression('Voice 1')
    measures.timespan.set_rhythm(rhythm_set_expression)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_from_past_07():
    '''Rhythm set expression lookup expression dependent leaf select expression start offset.
    Source is parseable string.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8), (5, 8)])
    measures = red_segment.select_measures('Voice 1')[1:3]
    red_segment.set_rhythm("{ c'8 [ c'8 ] }")
    measures.timespan.set_rhythm("{ c'16 [ c'16 c'16 ] }")
    blue_segment.set_rhythm("{ c'32 [ c'32 c'32 c'32 ] }")
    measures = blue_segment.select_measures('Voice 1')[1:3]
    leaves = red_segment.select_leaves('Voice 1')[:4]
    rhythm_set_expression = leaves.timespan.start_offset.look_up_rhythm_set_expression('Voice 1')
    measures.timespan.set_rhythm(rhythm_set_expression)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_rhythm_set_expression_from_past_08():
    '''Rhythm set expression lookup expression dependent leaf select expression stop offset.
    Source is parseable string.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8), (5, 8)])
    measures = red_segment.select_measures('Voice 1')[1:3]
    red_segment.set_rhythm("{ c'8 [ c'8 ] }")
    measures.timespan.set_rhythm("{ c'16 [ c'16 c'16 ] }")
    blue_segment.set_rhythm("{ c'32 [ c'32 c'32 c'32 ] }")
    measures = blue_segment.select_measures('Voice 1')[1:3]
    leaves = red_segment.select_leaves('Voice 1')[:4]
    rhythm_set_expression = leaves.timespan.stop_offset.look_up_rhythm_set_expression('Voice 1')
    measures.timespan.set_rhythm(rhythm_set_expression)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
