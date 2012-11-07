from abjad import *
from experimental import *


def test_multiple_segment_solo__reset_division_selectors_01():
    '''Reset persistent selectors.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures(4 * [(3, 16)])
    segment.set_divisions([(1, 16)], truncate=True)
    middle_two_measures = segment.select_segment_ratio_part((1, 2, 1), 1)
    segment.set_divisions([(2, 16)], selector=middle_two_measures, persist=True)
    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.append_segment('blue')
    segment.set_time_signatures(4 * [(2, 8)])
    segment.set_divisions([(3, 16)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_multiple_segment_solo__reset_division_selectors_02():
    '''Reset nonpersistent selectors.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment('red')
    segment.set_time_signatures(4 * [(3, 16)])
    segment.set_divisions([(1, 16)], truncate=False)
    middle_two_measures = segment.select_segment_ratio_part((1, 2, 1), 1)
    segment.set_divisions([(2, 16)], selector=middle_two_measures, persist=True)
    segment.set_rhythm(library.thirty_seconds)
    segment = score_specification.append_segment('blue')
    segment.set_time_signatures(4 * [(2, 8)])
    segment.set_divisions([(3, 16)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
