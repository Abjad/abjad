from experimental import *


def test_SegmentSpecification__set_rhythm_with_rotation_indicator_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = expressiontools.ScoreSpecificationInterface(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    divisions = red_segment.timespan.divide_by_ratio([1, 1, 1])
    red_segment.set_divisions(divisions)
    first_division = red_segment.select_divisions('Voice 1')[:1]
    second_division = red_segment.select_divisions('Voice 1')[1:2]
    third_division = red_segment.select_divisions('Voice 1')[2:3]
    first_division.timespan.set_rhythm(library.eighths)
    second_division.timespan.set_rhythm(library.sixteenths)
    third_division.timespan.set_rhythm(library.thirty_seconds)
    red_rhythm = red_segment.select_leaves('Voice 1')
    indicator = expressiontools.RotationIndicator(-1, 1)
    red_segment.set_rhythm(red_rhythm.rotate(indicator), contexts=['Voice 2'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
