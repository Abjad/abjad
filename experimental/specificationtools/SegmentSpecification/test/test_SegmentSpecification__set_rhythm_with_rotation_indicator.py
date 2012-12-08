from abjad import *
from experimental import *


def test_SegmentSpecification__set_rhythm_with_rotation_indicator_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    divisions = red_segment.request_partitioned_time('Voice 1', [1, 1, 1])
    red_segment.set_divisions(divisions)
    first_division = red_segment.select_divisions(0, 1)
    second_division = red_segment.select_divisions(1, 2)
    third_division = red_segment.select_divisions(2, 3)
    red_segment.set_rhythm(library.eighths, selector=first_division)
    red_segment.set_rhythm(library.sixteenths, selector=second_division)
    red_segment.set_rhythm(library.thirty_seconds, selector=third_division)
    red_rhythm = red_segment.request_rhythm('Voice 1')
    indicator = settingtools.RotationIndicator(-1, 1)
    red_segment.set_rhythm(red_rhythm, contexts=['Voice 2'], rotation=indicator)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
