from abjad import *
from experimental import *


def test_single_segment_solo__nonoverlapping_division_selectors_01():
    '''Nonoverlapping background measure selectors.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    first_measure = segment.select_background_measure(0)
    segment.set_divisions([(2, 32)], selector=first_measure)
    second_measure = segment.select_background_measure(1)
    segment.set_divisions([(3, 32)], selector=second_measure)
    third_measure = segment.select_background_measure(2)
    segment.set_divisions([(4, 32)], selector=third_measure)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
