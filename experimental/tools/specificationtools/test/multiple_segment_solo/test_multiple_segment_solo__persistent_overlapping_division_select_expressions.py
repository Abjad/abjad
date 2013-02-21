from experimental import *


def test_multiple_segment_solo__persistent_overlapping_division_select_expressions_01():
    '''Persistent overlapping measure division select expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(3, 16)])
    red_segment.set_divisions([(1, 16)], truncate=True)
    middle_two_measures = red_segment.select_measures('Voice 1')[1:3]
    middle_two_measures.timespan.set_divisions([(2, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(4 * [(2, 8)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo__persistent_overlapping_division_select_expressions_02():
    '''Persistent overlapping measures ratio part division select expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(3, 16)])
    red_segment.set_divisions([(1, 16)], truncate=True)
    measures = red_segment.select_measures('Voice 1')
    middle_two_measures = measures.partition_by_ratio((1, 2, 1))[1]
    middle_two_measures.timespan.set_divisions([(2, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(4 * [(2, 8)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo__persistent_overlapping_division_select_expressions_03():
    '''Persistent overlapping segment offsets division select expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(3, 16)])
    red_segment.set_divisions([(1, 16)], truncate=True)
    middle_two_measures = red_segment.timespan.translate((3, 16))
    middle_two_measures = middle_two_measures.set_duration((6, 16))
    middle_two_measures.set_divisions([(2, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(4 * [(2, 8)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo__persistent_overlapping_division_select_expressions_04():
    '''Persistent overlapping segment ratio part division select expression.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(3, 16)])
    red_segment.set_divisions([(1, 16)], truncate=True)
    middle_two_measures = red_segment.timespan.divide_by_ratio((1, 2, 1))[1]
    middle_two_measures.set_divisions([(2, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(4 * [(2, 8)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo__persistent_overlapping_division_select_expressions_05():
    '''Persistent overlapping measure division select expression can be overwritten.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(3, 16)])
    red_segment.set_divisions([(1, 16)])
    middle_two_measures = red_segment.select_measures('Voice 1')[1:3]
    middle_two_measures.timespan.set_divisions([(2, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(4 * [(2, 8)])
    middle_two_measures = blue_segment.select_measures('Voice 1')[1:3]
    middle_two_measures.timespan.set_divisions([(3, 16)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
