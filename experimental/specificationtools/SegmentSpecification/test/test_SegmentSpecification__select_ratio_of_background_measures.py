from abjad.tools import *
from experimental import *


def test_SegmentSpecification__select_ratio_of_background_measures_01():
    '''Count ratio part.
    '''
    
    template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    measures = red_segment.select_background_measure_timespan()
    left, right = selector = red_segment.select_count_ratio_parts(measures, (1, 1))
    red_segment.set_divisions([(3, 16)], selector=left, truncate=True)
    red_segment.set_divisions([(5, 16)], selector=right, truncate=True)
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_ratio_of_background_measures_02():
    '''Count ratio part.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    measures = red_segment.select_background_measure_timespan()
    last_two_measures = red_segment.select_count_ratio_parts(measures, (1, 1))[-1]
    red_segment.set_divisions([(2, 32)])
    red_segment.set_divisions([(3, 32)], selector=last_two_measures)
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_ratio_of_background_measures_03():
    '''Time ratio part.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    measures = red_segment.select_background_measure_timespan()
    last_measure = red_segment.select_time_ratio_parts(measures, (1, 1))[-1]
    red_segment.set_divisions([(2, 32)])
    red_segment.set_divisions([(3, 32)], selector=last_measure)
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
