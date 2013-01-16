from abjad import *
from experimental import *


def test_single_segment_solo__nonoverlapping_division_selectors_01():
    '''Nonoverlapping measure selectors.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    first_measure = red_segment.select_measures('Voice 1')[:1]
    first_measure.set_divisions([(2, 32)])
    second_measure = red_segment.select_measures('Voice 1')[1:2]
    second_measure.set_divisions([(3, 32)])
    third_measure = red_segment.select_measures('Voice 1')[2:3]
    third_measure.set_divisions([(4, 32)])
    red_segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
