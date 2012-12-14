from abjad import *
from experimental import *


def test_BackgroundMeasureSelector__set_rhythm_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(4 * [(2, 8)])
    red_segment.set_rhythm(library.sixteenths)
    measures = red_segment.select_background_measures(1, 3)
    measures.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
