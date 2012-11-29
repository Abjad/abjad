from abjad import *
from experimental import *


def test_single_segment_solo__overlapping_rhythm_selectors_01():
    '''Second selector equals first.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    red_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__overlapping_rhythm_selectors_02():
    '''Second selector delays the first.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    first_two_measures = red_segment.select_background_measures(stop=2)
    red_segment.set_rhythm(library.sixteenths, selector=first_two_measures)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__overlapping_rhythm_selectors_03():
    '''Second selector curtails the first.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    first_two_measures = red_segment.select_background_measures(start=-2)
    red_segment.set_rhythm(library.sixteenths, selector=first_two_measures)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__overlapping_rhythm_selectors_04():
    '''First selector properly contains the second.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(2, 8)])
    red_segment.set_divisions([(3, 16)])
    red_segment.set_rhythm(library.thirty_seconds)
    first_two_measures = red_segment.select_background_measures(1, 2)
    red_segment.set_rhythm(library.sixteenths, selector=first_two_measures)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__overlapping_rhythm_selectors_05():
    '''With rhythm material request.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(3, 8), (4, 8), (3, 8)])
    red_segment.set_rhythm("{ c'4 }")
    first_measure = red_segment.select_background_measures(0, 1)
    rhythmic_cell = score_specification.request_rhythm('Voice 1', selector=first_measure)
    last_measure = red_segment.select_background_measures(-1)
    red_segment.set_rhythm(rhythmic_cell, selector=last_measure)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
