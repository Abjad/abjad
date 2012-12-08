from abjad import *
from experimental import *


def test_SegmentSymbolicTimespan__divide_by_ratio_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    second_half_of_segment = red_segment.timespan.divide_by_ratio((1, 1))[-1]
    red_segment.set_divisions([(2, 16)])
    red_segment.set_divisions([(3, 16)], selector=second_half_of_segment)
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSymbolicTimespan__divide_by_ratio_02():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (1, 8), (1, 8), (3, 8)])
    middle_third_of_segment = red_segment.timespan.divide_by_ratio((1, 1, 1))[1]
    red_segment.set_divisions([(2, 16)])
    red_segment.set_divisions([(3, 16)], selector=middle_third_of_segment)
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
