from abjad import *
from experimental import *


def test_multiple_segment_solo__reset_division_selectors_01():
    '''Reset persistent selectors.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(3, 16)])
    red_segment.set_divisions([(1, 16)], truncate=True)
    middle_two_measures = red_segment.timespan.divide_by_ratio((1, 2, 1))[1]
    middle_two_measures.set_divisions([(2, 16)], persist=True)
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(4 * [(2, 8)])
    blue_segment.set_divisions([(3, 16)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo__reset_division_selectors_02():
    '''Reset nonpersistent selectors.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(3, 16)])
    red_segment.set_divisions([(1, 16)], truncate=False)
    middle_two_measures = red_segment.timespan.divide_by_ratio((1, 2, 1))[1]
    middle_two_measures.set_divisions([(2, 16)], persist=True)
    red_segment.set_rhythm(library.thirty_seconds)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(4 * [(2, 8)])
    blue_segment.set_divisions([(3, 16)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
