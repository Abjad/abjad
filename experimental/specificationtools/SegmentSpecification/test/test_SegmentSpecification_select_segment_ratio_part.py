from abjad import *
from experimental import *


def test_SegmentSpecification_select_segment_ratio_part_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.make_segment('red')
    segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    second_half_of_segment = segment.select_segment_ratio_part((1, 1), -1)
    segment.set_divisions([(2, 16)])
    segment.set_divisions([(3, 16)], selector=second_half_of_segment)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_select_segment_ratio_part_02():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.make_segment('red')
    segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    middle_third_of_segment = segment.select_segment_ratio_part((1, 1, 1), 1)
    segment.set_divisions([(2, 16)])
    segment.set_divisions([(3, 16)], selector=middle_third_of_segment)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
