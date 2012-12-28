from abjad import *
from experimental.tools import *


def test_BackgroundMeasureSelector__request_modifiers_01():
    '''Measures __getitem__().
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_background_measures('Voice 1')
    measures = measures[1:3]
    measures.set_rhythm(library.eighths)
    score = score_specification.interpret()
    
    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_BackgroundMeasureSelector__request_modifiers_02():
    '''Partition measures by ratio of counts.
    '''

    template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    measures = red_segment.select_background_measures('Voice 1')
    left, right = measures.partition_objects_by_ratio((1, 1))
    left.set_rhythm(library.sixteenths)
    right.set_rhythm(library.eighths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_BackgroundMeasureSelector__request_modifiers_03():
    '''Partition measures by ratio of durations.
    '''

    template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    measures = red_segment.select_background_measures('Voice 1')
    left, right = measures.partition_objects_by_ratio_of_durations((1, 1))
    left.set_rhythm(library.sixteenths)
    right.set_rhythm(library.eighths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_BackgroundMeasureSelector__request_modifiers_04():
    '''Repeat measures to length.
    '''

    template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_background_measures('Voice 1')
    measures = measures.repeat_to_length(2)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(measures)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_BackgroundMeasureSelector__request_modifiers_05():
    '''Repeat measures to duration.
    '''

    template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_background_measures('Voice 1')
    measures = measures.repeat_to_duration(Duration((9, 16)))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(measures)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_BackgroundMeasureSelector__request_modifiers_05():
    '''Reverse measures.
    '''

    template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_background_measures('Voice 1')
    measures = measures.reverse()
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(measures)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_BackgroundMeasureSelector__request_modifiers_06():
    '''Rotate measures.
    '''

    template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8), (4, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_background_measures('Voice 1')
    measures = measures.rotate(-1)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(measures)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
