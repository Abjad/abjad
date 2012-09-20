from abjad.tools import *
from experimental import *


def test_SegmentSpecification_select_background_measures_ratio_part_01():
    '''Count ratio part.
    '''
    
    template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(template)

    segment = score_specification.make_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])

    selector = segment.select_background_measures_ratio_part((1, 1), 0)
    segment.set_divisions([(3, 16)], selector=selector, truncate=True)

    selector = segment.select_background_measures_ratio_part((1, 1), 1)
    segment.set_divisions([(5, 16)], selector=selector, truncate=True)

    segment.set_rhythm(library.thirty_seconds)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_select_background_measures_ratio_part_02():
    '''Count ratio part.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.make_segment('red')
    segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    last_two_measures = segment.select_background_measures_ratio_part((1, 1), -1)
    segment.set_divisions([(2, 32)])
    segment.set_divisions([(3, 32)], selector=last_two_measures)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_select_background_measures_ratio_part_03():
    '''Time ratio part.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.make_segment('red')
    segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    last_measure = segment.select_background_measures_ratio_part((1, 1), -1, is_count=False)
    segment.set_divisions([(2, 32)])
    segment.set_divisions([(3, 32)], selector=last_measure)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
